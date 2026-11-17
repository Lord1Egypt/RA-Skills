# -*- coding: utf-8 -*-
"""adapters/qwenwork.py — 千问办公（QwenWork）数据源适配器

把千问办公本机的三类落地数据归一化为 agent-analytics-report 的统一
trace / session schema，复用同一套聚合与报告渲染逻辑，无需 WorkBuddy 环境。

千问办公的会话内核是 qoder-agent-sdk（与 Claude Code 同构），转录格式相近，
但**用量口径完全不同**：

  ┌─ 数据源 ─────────────────────────────────────────────────────────────┐
  │ 1. ~/.qwenworkcn/projects/<projectSlug>/<sessionId>.jsonl            │
  │    逐行 JSON 转录（user / assistant / runtime-config / …），含完整对话│
  │    内容、cwd、时间戳、模型档位、requestTokenAnchor.requestId         │
  │ 2. ~/.qwenworkcn/logs/runs/<run_id>/{manifest.json, qodercli.log}    │
  │    进程级运行日志：manifest 给出 run→session 映射与 CLI 版本；       │
  │    qodercli.log 的 model.request.started / model.response.completed  │
  │    是**逐次模型调用**的权威计数、模型档位与真实端到端耗时            │
  │ 3. %APPDATA%/QwenWorkCN/data/agents.db（SQLite，只读打开）            │
  │    chats / sub_chats / messages：真实会话标题、档位 model_level、     │
  │    每轮 durationMs 与 numTurns                                        │
  └──────────────────────────────────────────────────────────────────────┘

⚠️ 关键事实（本机实测，决定了本适配器的成本口径）
  千问办公上游**不回传 token 用量**：qodercli.log 中 1167 条
  `model.response.completed` 的 input_tokens / output_tokens /
  cache_read_input_tokens / cache_creation_input_tokens 全为 0，JSONL 的
  message.usage 恒为 null，agents.db 全文无 token / usage / credit 字段。
  → 调用次数、模型档位、请求耗时、会话标题、对话内容是**真实值**；
  → token 只能按**字符启发式估算**（见 estimate_tokens），成本一律 L2 估算级；
  → 千问办公按积分订阅计费，账号级积分无法归因到单个会话，**没有 L1 真值可对账**
    （这是与 WorkBuddy 源 + --import-official 最大的差别）。
  → 一旦上游开始回传真实 token，本适配器自动改用真实值
    （见 `_parse_session_file` 里的 `estimated` 判定），无需改代码。

两处噪声数据的处理（否则头条数字会被后台任务占满）
  - `model: "<synthetic>"` 的 assistant 消息是**中断 / 错误的占位**，不是一次真实
    模型调用 → 不计入 trace，只记进会话的 `_synthetic_responses` 计数。
  - 千问办公的**记忆整理后台任务**（注入提问以「Target file this round:」开头）
    确实花额度，但不是用户的任务 → 会话标 `is_background_automation=True` 并给
    可读名「记忆整理后台任务（awareness nudge）」，报告据此把它从 Top 榜摘出去。

计价
  trace 的 model_key 统一为 `qwenwork:<档位>`（档位取服务端下发的标识符，如
  flash / pro / qwork-lite / qmodel_latest）。千问办公没有公开的单 token 刊例价，
  故 pricing.json 里**故意不配**这些档位：未命中单价时按技能既有约定处理
  （计入 token、不计成本、报告中给出补价提示）。想看到金额，在
  scripts/pricing.local.json 里按裸档位名补价即可（price_of 会剥掉前缀查表）：
      {"flash": {"input": 1.2, "output": 4.8}, "pro": {"input": 7.2, "output": 28.8}}
"""

import hashlib
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

_HERE = Path(os.path.dirname(os.path.abspath(__file__)))
_SCRIPTS = _HERE.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ca_core import (  # noqa: E402
    CACHE_DISCOUNT,
    call_time_of,
    effective_tokens_of,
    is_scheduled_free,
    is_timed_free,
    iso_to_date,
    normalize_model,
    price_of,
    resolve_model,
)
from ca_sessions import classify_task  # noqa: E402

__all__ = [
    "QWENWORK_CHANNEL",
    "collect_qwenwork",
    "collect_qwenwork_sessions",
    "collect_qwenwork_traces",
    "estimate_tokens",
    "load_db_index",
    "load_run_usage",
    "resolve_qwenwork_db",
    "resolve_qwenwork_home",
]

# 本适配器产出的 trace 统一走此通道（ca_core.parse_channel 识别 qwenwork: 前缀）
QWENWORK_CHANNEL = "qwenwork"

# 显式能力声明：千问办公**在语义上不支持「计费」维度**，而不是「这次恰好没配单价」。
# 依据：① 积分订阅制、无公开单 token 刊例价；② 账号级积分无法归因到单个会话，
# 因此即便用户在 pricing.local.json 里填了档位单价，算出来的 ¥ 也是无法对账的虚构值。
# 生成器据此压制「本期有未配置单价的模型 + pricing.local.json 补价 stub」整块
# （见 generate_report._show_unconfigured_block），不靠「单价全 0」隐式推断——
# 将来千问真出可计价套餐时，把这个标记改成 True 即可，无需回头改渲染逻辑。
SUPPORTS_COST = False

_UNKNOWN_MODEL = "qwenwork-default"

# 占位响应：千问办公在中断 / 错误 / 后台任务里会写一条 `model: "<synthetic>"`
# 的 assistant 消息，它**不是一次真实的模型调用**（上游没有请求发出），
# 计入会虚增调用次数并把注入的大段上下文算成 input token。
_SYNTHETIC_MODELS = {"<synthetic>", "synthetic"}

# 后台自动任务指纹：千问办公的记忆整理（awareness nudge）会以
# 「Target file this round: …」作为注入提问跑在独立会话里。
# 它们确实花了额度，但不是用户的任务，故标 is_background_automation
# 让报告把它们从「Top 任务」榜单里摘出去，单独归口。
_BACKGROUND_TITLE_HINTS = ("Target file this round:",)
_BACKGROUND_TITLE = "记忆整理后台任务（awareness nudge）"

# ── 技能 / 产出物 / 自动化的本机信号源（WorkBuddy 三者都是独立数据源，千问办公不是）──
# 技能调用：转录里 tool_use name="Skill" → input.skill。~/.qwenworkcn/skill-usage.json
# 只有累计 usageCount（本机实测 2 条 vs 转录 17 次调用，低估约 8.5 倍），故只当旁证。
_SKILL_TOOL_NAME = "Skill"
# 交付物：present_files 工具（语义=「已作为交付物呈现给用户」），工具名带 MCP 前缀且
# 版本间可能改名，故用子串匹配而非硬枚举全名。
_PRESENT_TOOL_HINT = "present_files"
# 改过的文件（单独计数，不进交付清单：Edit 本机 3305 次会把清单淹掉）
_WRITE_TOOLS = ("Write", "Edit", "NotebookEdit")
# 交付物磁盘兜底目录名（千问办公每个 chat 一个 workspace/<chatId>/outputs）
_OUTPUTS_DIR_NAME = "outputs"
# 磁盘扫描时跳过的备份/临时产物（present_files 显式交付的文件一律照单收，不筛）：
# 只扫磁盘会把 `xxx.json.2026....bak`、`~$xxx.docx` 这类当成"交付物"灌进 §九。
_DISK_SKIP_SUFFIXES = (".bak", ".tmp", ".temp", ".swp", "~")
_DISK_SKIP_PREFIXES = ("~$", ".")
# task_run_logs.status 的成功态（不同版本字面量不一，一律小写比对；
# 未列出的状态一律算失败，宁可少报成功也不把未知态当成功）
_AUTO_SUCCESS_STATES = {"success", "succeeded", "completed", "complete", "ok", "done"}


def _norm_path_key(path):
    """路径归一化做去重键：统一分隔符 + 小写（Windows 大小写不敏感）。"""
    return str(path or "").replace("\\", "/").strip().rstrip("./").lower()


def _deliverable(path, date=None, source="present_files"):
    """把一条文件路径摊成 §九 渲染层要的 file_name/extension/size_bytes/date。

    size 走 os.stat（文件已被清理则给 0，不抛异常也不猜）；date 优先用调用时刻，
    仅磁盘扫描命中（没有调用时间可考）时退到文件 mtime 的北京时间日期。
    额外带 `path` / `source` / `missing` 三个透明字段，渲染层不读但便于排查与测试。
    """
    p = Path(str(path))
    size = 0
    try:
        st = p.stat()
        size = int(getattr(st, "st_size", 0) or 0)
        if not date:
            date = iso_to_date(_ms_to_iso(int(st.st_mtime * 1000))) or ""
    except (OSError, ValueError):
        pass
    return {"file_name": p.name or str(path),
            "extension": (p.suffix or "").lstrip(".").lower(),
            "size_bytes": size,
            "path": str(path),
            "date": date or "",
            "source": source,
            "missing": size == 0}

# ── token 估算系数（保守口径，集中在此便于复核调参）─────────────────────────
# CJK 字符：Qwen 系 BPE 实测约 0.6~1.0 token/字，取 1.0 偏高估——
# 宁可高估用量，也不要把成本算少。
CJK_TOKENS_PER_CHAR = 1.0
# 非 CJK（拉丁、数字、符号、JSON 结构符）：业界经验 3.5~4.3 字符/token，取 4.0。
LATIN_CHARS_PER_TOKEN = 4.0

_CJK_RE = re.compile(
    "["
    "\u3040-\u30ff"   # 日文假名
    "\u3400-\u4dbf"   # 中文扩展 A
    "\u4e00-\u9fff"   # 中文基本区
    "\uac00-\ud7af"   # 韩文音节
    "\uf900-\ufaff"   # CJK 兼容表意文字
    "\uff00-\uffef"   # 全角标点
    "]+",
    re.UNICODE,
)
_UUID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}"
                      r"-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")

# ── qodercli.log 行解析 ─────────────────────────────────────────────────────
# 毫秒位在不同 CLI 版本里可有可无，做成可选，避免整行被丢弃
_LOG_TS_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?[+-]\d{2}:\d{2})")
_REQ_ID_RE = re.compile(r'request_id="(' + _UUID_RE.pattern + r')"')
_SESSION_RE = re.compile(r"\bsession=(" + _UUID_RE.pattern + r")")
_MODEL_RE = re.compile(r'\bmodel="([^"]+)"')
_STOP_RE = re.compile(r'\bstop_reason="([^"]*)"')
_TOKEN_KEYS = ("input_tokens", "output_tokens", "cache_read_input_tokens",
               "cache_creation_input_tokens")
_TOKEN_RE = {k: re.compile(r"\b%s=(\d+)" % k) for k in _TOKEN_KEYS}


# ── 路径探测 ────────────────────────────────────────────────────────────────

def resolve_qwenwork_home():
    """定位千问办公资源目录（其下为 projects/ 与 logs/runs/）。

    优先级：
      1. 环境变量 QWENWORK_HOME —— 直接指向主目录（测试与自定义安装位）
      2. 平台默认候选（取第一个存在者）：~/.qwenworkcn、~/.qwenwork
    返回 Path；目录可能不存在（本机未装千问办公），调用方负责判空。
    """
    env = os.environ.get("QWENWORK_HOME")
    if env:
        return Path(env).expanduser()
    home = Path.home()
    candidates = [home / ".qwenworkcn", home / ".qwenwork"]
    for c in candidates:
        if c.is_dir():
            return c
    return candidates[0]


def resolve_qwenwork_db(home=None):
    """定位千问办公业务库 agents.db（只读打开；不存在时返回首选默认路径）。

    优先级：QWENWORK_DB 环境变量 →
      Windows: %APPDATA%/QwenWorkCN/data/agents.db
      macOS/Linux: $XDG_CONFIG_HOME/QwenWorkCN/data/agents.db（默认 ~/.config/...）
    """
    env = os.environ.get("QWENWORK_DB")
    if env:
        return Path(env).expanduser()
    candidates = []
    if os.name == "nt":  # Windows
        appdata = os.environ.get("APPDATA")
        base = Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"
        candidates.append(base / "QwenWorkCN" / "data" / "agents.db")
    else:
        xdg = os.environ.get("XDG_CONFIG_HOME")
        base = Path(xdg) if xdg else Path.home() / ".config"
        candidates.append(base / "QwenWorkCN" / "data" / "agents.db")
    for c in candidates:
        if c.exists():
            return c
    return candidates[0]


def _projects_root(home):
    return Path(home) / "projects"


def _runs_root(home):
    return Path(home) / "logs" / "runs"


# ── 基础工具 ────────────────────────────────────────────────────────────────

def estimate_tokens(text):
    """字符启发式 token 估算：CJK 逐字计 1，其余按 4 字符折 1。

    千问办公上游不回传 token，本函数是**唯一的 token 来源**，故报告里的 token
    数字全部是估算值，须按 L2 口径解读（结构性结论可信，金额与用量当趋势看）。
    """
    if not text:
        return 0
    s = text if isinstance(text, str) else str(text)
    cjk = sum(len(m) for m in _CJK_RE.findall(s))
    other = len(s) - cjk
    return int(cjk * CJK_TOKENS_PER_CHAR + other / LATIN_CHARS_PER_TOKEN + 0.5)


def _stable_pid(seed):
    """从字符串生成稳定非负 int（模拟 WorkBuddy 的 pid_dir.name → int）。"""
    h = hashlib.sha256(str(seed).encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def _ts_to_ms(iso_str):
    """ISO 8601（Z 或 ±HH:MM）或毫秒时间戳 → Unix 毫秒（异常返回 0）。

    Windows 上 datetime.timestamp() 对 1970 年前的时刻会抛 OSError，
    历史转录里混着这类脏时间戳，一律降级为 0（该条不计入时间窗）。
    """
    if not iso_str:
        return 0
    if isinstance(iso_str, (int, float)):
        v = int(iso_str)
        if v <= 0:
            return 0
        # 秒级时间戳（10 位）自动补齐为毫秒，避免落到 1970 年
        return v * 1000 if v < 100_000_000_000 else v
    try:
        dt = datetime.fromisoformat(str(iso_str).replace("Z", "+00:00"))
        return int(dt.timestamp() * 1000)
    except (ValueError, TypeError, OSError):
        return 0


def _ms_to_iso(ms):
    """Unix 毫秒 → ISO 8601（UTC），供 created_date 兜底。"""
    if not ms:
        return ""
    try:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).isoformat()
    except (ValueError, TypeError, OSError):
        return ""


def _to_int(v, default=0):
    try:
        return int(v)
    except (TypeError, ValueError):
        return default


def _iter_lines(path):
    """读文本文件的行（编码容错，OSError 时静默返回）。"""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            for ln in fh:
                yield ln
    except (OSError, IOError):
        return


def _read_jsonl_lines(path):
    """逐行读取 JSONL，坏行静默跳过（与 collect_traces 的容错一致）。"""
    for ln in _iter_lines(path):
        ln = ln.strip()
        if not ln:
            continue
        try:
            yield json.loads(ln)
        except (json.JSONDecodeError, TypeError, ValueError):
            continue


def _block_text(blk):
    """把 content block 摊平成用于估算 token 的纯文本。

    覆盖 text / thinking / tool_use / tool_result；未知块整体 JSON 化——
    工具入参与回显都是**真实进过上下文的内容**，不计数会明显低估用量。
    """
    if blk is None:
        return ""
    if isinstance(blk, str):
        return blk
    if not isinstance(blk, dict):
        return ""
    typ = blk.get("type")
    if typ in ("text", "input_text", "output_text"):
        return blk.get("text") or blk.get("content") or ""
    if typ == "thinking":
        return blk.get("thinking") or ""
    if typ == "tool_use":
        try:
            payload = json.dumps(blk.get("input"), ensure_ascii=False)
        except (TypeError, ValueError):
            payload = str(blk.get("input"))
        return "%s %s" % (blk.get("name") or "", payload)
    if typ == "tool_result":
        c = blk.get("content")
        if isinstance(c, list):
            return " ".join(_block_text(x) for x in c)
        return c or ""
    try:
        return json.dumps(blk, ensure_ascii=False)
    except (TypeError, ValueError):
        return ""


def _message_text(message):
    """抽取一条 message 的全部文本（content 为 str 或 block 列表）。"""
    if not isinstance(message, dict):
        return ""
    c = message.get("content")
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        return " ".join(_block_text(b) for b in c)
    return ""


# ── 运行日志：逐次调用的权威计数与真实耗时 ──────────────────────────────────

def _manifest_session_ids(manifest_path):
    """从 run 的 manifest.json 取出该进程服务过的 sessionId 集合。

    manifest.argv 里是 [..., "--session-id", "<uuid>", ...]；同时兜底全文扫 uuid
    （千问办公会把 sessionId 写进 argv 之外的若干字段，且不同版本字段位置不一）。
    """
    try:
        raw = manifest_path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, IOError):
        return set()
    ids = set()
    try:
        man = json.loads(raw)
    except (json.JSONDecodeError, TypeError, ValueError):
        man = None
    if isinstance(man, dict):
        argv = man.get("argv") or []
        if isinstance(argv, list):
            for i, a in enumerate(argv):
                if a == "--session-id" and i + 1 < len(argv) and isinstance(argv[i + 1], str):
                    ids.add(argv[i + 1])
    ids.update(_UUID_RE.findall(raw))
    return ids


def _parse_run_log(log_path):
    """解析单个 qodercli.log → {request_id: 用量摘要}。

    摘要：session_id / model / started_ts / completed_ts / duration_ms /
    stop_reason / tokens（四个上游字段，当前恒为 0；非 0 时会被自动采用）。
    """
    out = {}
    started = {}  # request_id -> (起始毫秒, session_id)
    for ln in _iter_lines(log_path):
        if "model.request.started" not in ln and "model.response.completed" not in ln:
            continue
        ts_m = _LOG_TS_RE.match(ln)
        rid_m = _REQ_ID_RE.search(ln)
        if not ts_m or not rid_m:
            continue
        rid = rid_m.group(1)
        ms = _ts_to_ms(ts_m.group(1))
        sess_m = _SESSION_RE.search(ln)
        sess = sess_m.group(1) if sess_m else ""
        if "model.request.started" in ln:
            started[rid] = (ms, sess)
            continue
        rec = out.get(rid)
        if rec is None:
            st = started.get(rid, (0, ""))
            rec = {
                "request_id": rid,
                "session_id": sess or st[1],
                "model": "",
                "started_ts": st[0],
                "completed_ts": 0,
                "duration_ms": 0,
                "stop_reason": "",
                "tokens": {},
            }
            out[rid] = rec
        if not rec["session_id"]:
            rec["session_id"] = sess
        if rec["started_ts"] and ms:
            rec["duration_ms"] = max(ms - rec["started_ts"], 0)
        mm = _MODEL_RE.search(ln)
        if mm:
            rec["model"] = mm.group(1)
        sr = _STOP_RE.search(ln)
        if sr:
            rec["stop_reason"] = sr.group(1)
        for k, rx in _TOKEN_RE.items():
            g = rx.search(ln)
            if g:
                rec["tokens"][k] = int(g.group(1))
    return out


def load_run_usage(home, session_ids=None):
    """扫描 logs/runs/*/，返回 {request_id: 摘要}。

    session_ids 为 None 时全量扫描；否则只解析 manifest 命中的 run 日志，
    避免为了一个星期的数据把数百个日志文件读一遍。
    """
    runs = _runs_root(home)
    by_request = {}
    if not runs.is_dir():
        return by_request
    want = set(session_ids) if session_ids is not None else None
    try:
        entries = sorted(p for p in runs.iterdir() if p.is_dir())
    except OSError:
        return by_request
    for d in entries:
        man = d / "manifest.json"
        sids = _manifest_session_ids(man) if man.exists() else set()
        if want is not None and not (sids & want):
            continue
        log = d / "qodercli.log"
        if not log.exists():
            continue
        for rid, rec in _parse_run_log(log).items():
            if want is not None and rec.get("session_id") and rec["session_id"] not in want:
                continue
            by_request[rid] = rec
    return by_request


# ── agents.db：真实标题 / 档位 / 每轮耗时 ────────────────────────────────────

def load_db_index(db_path=None):
    """只读打开 agents.db → {session_id: 业务元信息}。

    元信息：title（界面上的会话真名）、cwd、model_level、mode、
    created_at / updated_at（毫秒）、num_turns、duration_ms（各轮求和）。
    库缺失 / 被锁 / schema 变更时返回 {}，适配器自动降级为纯 JSONL 口径。
    """
    index = {}
    con = _db_connect(db_path)
    if con is None:
        return index
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT sc.session_id, sc.model_level, sc.mode, sc.created_at, "
            "       sc.updated_at, c.name, c.worktree_path "
            "FROM sub_chats sc LEFT JOIN chats c ON c.id = sc.chat_id")
        for sid, level, mode, created, updated, name, wtp in cur.fetchall():
            if not sid:
                continue
            index[sid] = {
                "title": (name or "").strip(),
                "cwd": (wtp or "").strip(),
                "model_level": (level or "").strip(),
                "mode": (mode or "agent").strip(),
                "created_at": _to_int(created) * 1000,
                "updated_at": _to_int(updated) * 1000,
                "num_turns": 0,
                "duration_ms": 0,
            }
        try:
            cur.execute("SELECT metadata FROM messages WHERE metadata IS NOT NULL")
            for (meta,) in cur.fetchall():
                if not meta:
                    continue
                try:
                    d = json.loads(meta)
                except (json.JSONDecodeError, TypeError, ValueError):
                    continue
                if not isinstance(d, dict):
                    continue
                sid = d.get("sessionId")
                if not sid or sid not in index:
                    continue
                index[sid]["duration_ms"] += _to_int(d.get("durationMs"))
                index[sid]["num_turns"] = max(index[sid]["num_turns"],
                                              _to_int(d.get("numTurns")))
        except sqlite3.Error:
            pass
    except sqlite3.Error:
        return index
    finally:
        try:
            con.close()
        except sqlite3.Error:
            pass
    return index


# ── 单个会话转录解析 ────────────────────────────────────────────────────────

def _parse_session_file(path, start_date, end_date, run_usage=None):
    """解析一个 <sessionId>.jsonl → (traces, session_meta)。

    分组：千问办公把**一次模型响应**拆成多行（thinking / text / tool_use 各一行），
    它们共享同一个 requestTokenAnchor.requestId，故按该 id 归并成 1 条 trace。

    上下文推进：按文件顺序维护 ctx（已结算内容），每开一个新 group 就记录
    input_ctx = 当前 ctx。真实计费里 input ≈ 之前全部上下文的重发，这是无 usage
    回传时最贴近实际的估算方式（system prompt 不落盘，故实际 input 略高于估算）。
    """
    run_usage = run_usage or {}
    session_id = path.stem
    cwd = ""
    cli_version = ""
    human_texts = []
    dialogue_parts = []
    title = ""
    first_model = ""
    runtime_model = ""
    created_ms = None
    updated_ms = None
    groups = []
    group_by_key = {}
    ctx = 0  # 已结算进上下文的估算 token

    for obj in _read_jsonl_lines(path):
        if not isinstance(obj, dict):
            continue
        typ = obj.get("type")
        # 时间戳跨版本有两种形态：主会话是 ISO 8601 字符串，IM/渠道挂载会话是
        # 毫秒整数。统一归一（ts 供 iso_to_date 用，ms 供时间窗与排序用），
        # 否则 iso_to_date(整数) 会直接抛 AttributeError。
        ts_raw = obj.get("timestamp")
        ms = _ts_to_ms(ts_raw)
        ts = ts_raw if isinstance(ts_raw, str) else _ms_to_iso(ms)
        if ms:
            created_ms = ms if created_ms is None else min(created_ms, ms)
            updated_ms = ms if updated_ms is None else max(updated_ms, ms)
        if obj.get("sessionId"):
            session_id = obj["sessionId"]
        if obj.get("cwd"):
            cwd = obj["cwd"]
        if obj.get("version"):
            cli_version = str(obj["version"])

        if typ == "runtime-config":
            m = obj.get("model")
            if isinstance(m, str) and m:
                runtime_model = m
                first_model = first_model or m
            continue

        if typ == "user":
            hi = obj.get("humanInput")
            if isinstance(hi, dict) and hi.get("text"):
                txt = str(hi["text"]).strip()
                if txt:
                    human_texts.append(txt)
                    title = title or txt
                    dialogue_parts.append(txt)
            # 结清上一个 group 的输出（它此刻才真正进入后续请求的上下文），
            # 再计入本行内容——工具回显同样是真实的 input
            if groups and not groups[-1]["settled"]:
                ctx += groups[-1]["out_tokens"]
                groups[-1]["settled"] = True
            ctx += estimate_tokens(_message_text(obj.get("message")))
            continue

        if typ != "assistant":
            continue

        message = obj.get("message") or {}
        anchor = obj.get("requestTokenAnchor") or {}
        rid = ""
        if isinstance(anchor, dict):
            rid = anchor.get("requestId") or anchor.get("response") or ""
        key = rid or "%s#%d" % (ts, len(groups))
        model = message.get("model") if isinstance(message, dict) else ""
        model = model if isinstance(model, str) else ""
        g = group_by_key.get(key)
        if g is None:
            # 新响应开始：上一个 group 的输出此时才进入上下文
            if groups and not groups[-1]["settled"]:
                ctx += groups[-1]["out_tokens"]
                groups[-1]["settled"] = True
            g = {
                "request_id": key,
                "ts": ts,
                "ms": ms or 0,
                "model": model or runtime_model,
                "out_tokens": 0,
                "input_ctx": ctx,
                "blocks": 0,
                "texts": [],
                "skills": [],        # 本次响应里调用了哪些技能（[skill_id]，可重复）
                "presents": [],      # 本次响应里 present_files 交付的文件路径
                "writes": [],        # 本次响应里 Write/Edit 改动的文件路径（单独计数）
                "sidechain": bool(obj.get("isSidechain")),
                "settled": False,
            }
            group_by_key[key] = g
            groups.append(g)
        elif model and not g["model"]:
            g["model"] = model

        blocks = message.get("content") if isinstance(message, dict) else None
        if isinstance(blocks, str):
            blocks = [{"type": "text", "text": blocks}]
        if isinstance(blocks, list):
            for blk in blocks:
                txt = _block_text(blk)
                g["out_tokens"] += estimate_tokens(txt)
                g["blocks"] += 1
                # 只把助手正文喂给任务分类（thinking / 工具噪声会污染分类）
                if isinstance(blk, dict) and blk.get("type") == "text" and txt:
                    g["texts"].append(txt)
                elif isinstance(blk, dict) and blk.get("type") == "tool_use":
                    _tname = blk.get("name") or ""
                    _tinp = blk.get("input") if isinstance(blk.get("input"), dict) else {}
                    if _tname == _SKILL_TOOL_NAME and _tinp.get("skill"):
                        g["skills"].append(str(_tinp["skill"]))
                    elif _PRESENT_TOOL_HINT in _tname:
                        for _it in (_tinp.get("files") or []):
                            if isinstance(_it, dict) and _it.get("file_path"):
                                g["presents"].append(str(_it["file_path"]))
                    elif _tname in _WRITE_TOOLS and _tinp.get("file_path"):
                        g["writes"].append(str(_tinp["file_path"]))

    if groups and not groups[-1]["settled"]:
        ctx += groups[-1]["out_tokens"]
        groups[-1]["settled"] = True
    for g in groups:
        if g["texts"]:
            dialogue_parts.append(" ".join(g["texts"]))

    traces = []
    synthetic_skipped = 0
    for g in groups:
        date = iso_to_date(g["ts"])
        if not date or date < start_date or date > end_date:
            continue
        usage = run_usage.get(g["request_id"]) or {}
        # 占位响应（<synthetic>）不是一次真实调用，直接不计
        _raw_name = usage.get("model") or g["model"] or first_model or runtime_model or ""
        if _raw_name in _SYNTHETIC_MODELS:
            synthetic_skipped += 1
            continue
        real = usage.get("tokens") or {}
        in_tok = _to_int(real.get("input_tokens"))
        out_tok = _to_int(real.get("output_tokens"))
        cache_read = _to_int(real.get("cache_read_input_tokens"))
        # 上游回传了任一非 0 token → 采用真值；否则整体走字符估算
        estimated = not any(_to_int(real.get(k)) for k in _TOKEN_KEYS)
        if estimated:
            in_tok = g["input_ctx"]
            out_tok = g["out_tokens"]
        total = in_tok + out_tok
        model = _raw_name or _UNKNOWN_MODEL
        bare = normalize_model(model)
        model_key = "%s:%s" % (QWENWORK_CHANNEL, bare)
        pricing_model = resolve_model(bare)
        _when = call_time_of(g["ts"], date)
        ip, op = price_of(model_key, **_when)
        if ip is not None and op is not None:
            input_cost = (in_tok / 1_000_000) * ip
            output_cost = (out_tok / 1_000_000) * op
            cost = input_cost + output_cost
            eff_in = max(in_tok - cache_read * (1 - CACHE_DISCOUNT), 0)
            eff_cost = (eff_in / 1_000_000) * ip + (out_tok / 1_000_000) * op
        else:
            input_cost = output_cost = cost = eff_cost = 0.0
        eff_tokens = effective_tokens_of(total, cache_read)
        is_free = (is_timed_free(pricing_model, date)
                   or is_scheduled_free(pricing_model, **_when))
        started_ms = _to_int(usage.get("started_ts"))
        traces.append({
            "trace_id": "%s:%s:%d" % (session_id, g["ts"], len(traces)),
            "pid": _stable_pid(cwd or session_id),
            "date": date,
            "started_at": _ms_to_iso(started_ms) or g["ts"],
            "ended_at": g["ts"],
            "duration_ms": _to_int(usage.get("duration_ms")),
            "status": "success",
            "session_id": session_id,
            "total_tokens": total,
            "input_tokens": in_tok,
            "output_tokens": out_tok,
            "cached_tokens": cache_read,
            "call_count": 1,
            "models": [bare],
            "model_name": bare,
            "exec_model": bare,
            "model_key": model_key,
            "channel": QWENWORK_CHANNEL,
            "raw_model": model_key,
            "total_cost": round(cost, 4),
            "input_cost": round(input_cost, 4),
            "output_cost": round(output_cost, 4),
            "effective_tokens": eff_tokens,
            "effective_cost": round(eff_cost, 4),
            "is_free": is_free,
            # ── 透明字段：让读者一眼看清口径 ──
            "_tokens_estimated": estimated,
            "_request_id": g["request_id"],
            "_content_blocks": g["blocks"],
            "_is_sidechain": g["sidechain"],
            "_stop_reason": usage.get("stop_reason") or "",
        })

    if not title:
        title = human_texts[0] if human_texts else (Path(cwd).name if cwd else session_id)
    # 后台自动任务（记忆整理 nudge）确实花额度，但不是用户的任务：
    # 打上 is_background_automation 并给一个可读名，报告据此把它从 Top 榜摘出去
    is_bg = any(h in title for h in _BACKGROUND_TITLE_HINTS)
    # 技能调用与交付物：按窗口日期收敛（调用时刻即日期真值，无需估算）
    _skill_calls, _presents, _writes = [], [], []
    for g in groups:
        _d = iso_to_date(g["ts"])
        if not _d or _d < start_date or _d > end_date:
            continue
        for _s in g["skills"]:
            _skill_calls.append((_s, _d))
        for _p in g["presents"]:
            _presents.append((_p, _d))
        _writes.extend(g["writes"])

    session_meta = {
        "id": session_id,
        "cwd": cwd,
        "title": (_BACKGROUND_TITLE if is_bg else title[:60].strip()) or session_id,
        "custom_title": "",
        "status": "completed",
        "created_at": created_ms or 0,
        "created_date": iso_to_date(_ms_to_iso(created_ms)),
        "updated_at": updated_ms or 0,
        "mode": QWENWORK_CHANNEL,
        "model": ("%s:%s" % (QWENWORK_CHANNEL, normalize_model(first_model))
                  if first_model else QWENWORK_CHANNEL),
        "is_background_automation": is_bg,
        "version": cli_version or "unknown",
        "_dialogue_text": " ".join(dialogue_parts[:40]),
        "_human_turns": len(human_texts),
        "_request_count": len(groups),
        "_synthetic_responses": synthetic_skipped,
        # 三个新维度的原始素材，聚合在 _assemble 里做（跨会话去重才准确）
        "_skill_calls": _skill_calls,
        "_presents": _presents,
        "_writes": _writes,
    }
    return traces, session_meta


# ── 会话候选（避免全量读上百 MB 转录）───────────────────────────────────────

def _iter_session_files(projects_root, start_date, end_date, db_index):
    """枚举待解析的转录文件；两道闸，任一命中即保留（宁可多算不可漏算）。

      1. agents.db 的会话时间窗与请求窗口相交 → 保留（跨周长会话不会被漏）
      2. 文件 mtime 不早于 start_date - 2 天 → 保留（无 DB 或 DB 缺该会话时兜底）

    mtime 只当下界用，**不做上界**：mtime 只能证明「这个文件在这天之后还动过」，
    不能证明会话活动落在窗口内；真正的越界判断交给 trace 级日期过滤。
    """
    root = Path(projects_root)
    if not root.is_dir():
        return
    floor_ms = _ts_to_ms(start_date + "T00:00:00+00:00") - 2 * 86400 * 1000
    ceil_ms = _ts_to_ms(end_date + "T23:59:59+00:00") + 2 * 86400 * 1000
    try:
        files = sorted(root.rglob("*.jsonl"))
    except OSError:
        return
    for f in files:
        info = db_index.get(f.stem)
        keep = False
        if info:
            created = _to_int(info.get("created_at"))
            updated = _to_int(info.get("updated_at")) or created
            keep = bool(created and updated and created <= ceil_ms and updated >= floor_ms)
        if not keep:
            try:
                mtime = f.stat().st_mtime * 1000
            except OSError:
                mtime = 0
            keep = bool(mtime and mtime >= floor_ms)
        if keep:
            yield f


# ── 技能 / 交付物 / 自动化 / 后台运行 ────────────────────────────────────────

def _db_connect(db_path):
    """只读打开 agents.db；库缺失 / 被锁 / 非 sqlite 时返回 None（调用方降级）。"""
    path = Path(db_path) if db_path else resolve_qwenwork_db()
    if not path.exists():
        return None
    uri = "file:" + str(path).replace("\\", "/") + "?mode=ro"
    try:
        return sqlite3.connect(uri, uri=True, timeout=1.0)
    except sqlite3.Error:
        return None


def load_automation_runs(db_path=None, start_date=None, end_date=None):
    """定时任务运行记录 → 共享层 automation_runs 契约。

    字段必须凑齐五个：`collect_usage_data` 汇总时用 `r["result_success"]` **硬索引**，
    少一个 key 会把整次采集 KeyError 打崩（不是 .get）。`auto_status` 由
    `scheduled_tasks.enabled` 映射成 `_auto_is_active()` 认的 ACTIVE / PAUSED。
    本机没有定时任务时返回 []，此时报告里的「无自动化运行记录」是**真 0**。
    """
    con = _db_connect(db_path)
    if con is None:
        return []
    runs = []
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT r.task_id AS task_id, t.name AS name, t.enabled AS enabled, "
            "       r.run_at AS run_at, r.created_at AS created_at, "
            "       r.status AS status, r.duration_ms AS duration_ms "
            "FROM task_run_logs r LEFT JOIN scheduled_tasks t ON t.id = r.task_id "
            "ORDER BY r.created_at ASC")
        for row in cur.fetchall():
            ts_ms = _to_int(row[3]) * 1000 or _to_int(row[4]) * 1000
            date = iso_to_date(_ms_to_iso(ts_ms))
            if not date or (start_date and (date < start_date or date > end_date)):
                continue
            status = str(row[5] or "").strip().lower()
            runs.append({
                "automation_id": str(row[0] or "unknown"),
                "automation_name": (row[1] or str(row[0] or "定时任务")).strip(),
                # enabled 为 NULL（任务已删除、只剩 run 日志）时按 PAUSED 处理，
                # 不误报成「执行中自动化」
                "auto_status": "ACTIVE" if _to_int(row[2]) == 1 else "PAUSED",
                "result_success": status in _AUTO_SUCCESS_STATES,
                "created_date": date,
                "duration_ms": _to_int(row[6]),
                "error": "",
            })
    except sqlite3.Error:
        return []
    finally:
        try:
            con.close()
        except sqlite3.Error:
            pass
    return runs


def load_background_runs(db_path=None, start_date=None, end_date=None):
    """`nudge_logs` → 后台自动运行摘要（记忆整理 / 反思等）。

    **不塞进 automation_runs**：本机 317 条里只有 26 条能 join 到 sub_chats.session_id
    （会话归因率约 8%），进 §八 分组会造出一堆 unknown 组。这里只出全局计数与失败率，
    落 `meta.background_runs` 供 §一 那一行使用。
    """
    con = _db_connect(db_path)
    if con is None:
        return {}
    summary = {}
    try:
        cur = con.cursor()
        cur.execute("SELECT type, duration_ms, is_error, created_at FROM nudge_logs")
        count = err = dur = 0
        types = {}
        for typ, duration, is_err, created in cur.fetchall():
            date = iso_to_date(_ms_to_iso(_to_int(created) * 1000))
            if not date or (start_date and (date < start_date or date > end_date)):
                continue
            count += 1
            dur += _to_int(duration)
            if _to_int(is_err):
                err += 1
            key = str(typ or "unknown")
            types[key] = types.get(key, 0) + 1
        if count:
            summary = {"count": count, "error_count": err, "total_duration_ms": dur,
                       "types": dict(sorted(types.items(), key=lambda kv: -kv[1]))}
    except sqlite3.Error:
        return {}
    finally:
        try:
            con.close()
        except sqlite3.Error:
            pass
    return summary


def aggregate_skill_usage(sessions, active_days=None):
    """会话里的 `_skill_calls` → 共享层 skill_usage 契约（与 collect_skill_usage 同形）。

    `usage_count_in_range` 数的是**调用次数**（不去重），`recent_dates_in_range`
    是去重且有序的日期列表——§七 两张口径都用得到。
    """
    skills = {}
    for s in sessions:
        for skill, date in (s.get("_skill_calls") or []):
            e = skills.setdefault(skill, {"last_used": "", "first_seen": "",
                                           "recent_dates_in_range": [],
                                           "usage_count_in_range": 0})
            e["usage_count_in_range"] += 1
            if date not in e["recent_dates_in_range"]:
                e["recent_dates_in_range"].append(date)
            e["last_used"] = max(e["last_used"], date)
            e["first_seen"] = min(e["first_seen"], date) if e["first_seen"] else date
    for e in skills.values():
        e["recent_dates_in_range"] = sorted(e["recent_dates_in_range"])
    return {"skills": dict(sorted(skills.items(), key=lambda kv: -kv[1]["usage_count_in_range"])),
            "active_days": sorted(active_days or set())}


def collect_deliverables(sessions, start_date, end_date):
    """交付物清单：present_files 调用 ∪ 磁盘 <cwd>/outputs 扫描，按归一路径去重。

    两源的分工不是重复计数：present_files 才等于「交付给用户」，磁盘扫描兜住
    「写了但没走 present_files」的文件；同一文件两源都命中时保留 present_files 的
    调用日期（比 mtime 更贴近「什么时候产出的」）。
    """
    out = {}
    for s in sessions:
        for path, date in (s.get("_presents") or []):
            key = _norm_path_key(path)
            if key and key not in out:
                out[key] = _deliverable(path, date, source="present_files")
    for s in sessions:
        cwd = s.get("cwd")
        if not cwd:
            continue
        d = Path(cwd) / _OUTPUTS_DIR_NAME
        if not d.is_dir():
            continue
        try:
            entries = sorted(p for p in d.iterdir() if p.is_file())
        except OSError:
            continue
        for p in entries:
            name = p.name
            if name.endswith(_DISK_SKIP_SUFFIXES) or name.startswith(_DISK_SKIP_PREFIXES):
                continue      # 备份 / 临时 / 隐藏产物不算交付物（present_files 不筛）
            key = _norm_path_key(p)
            if key in out:
                continue      # 同一文件两源都命中时保留 present_files 的调用日期
            date = iso_to_date(_ms_to_iso(int(p.stat().st_mtime * 1000)))
            if not date or date < start_date or date > end_date:
                continue
            out[key] = _deliverable(p, date, source="disk_scan")
    return sorted(out.values(), key=lambda x: (x.get("date") or "", x.get("file_name") or ""))


# ── 对外入口 ────────────────────────────────────────────────────────────────

def _merge_session(a, b):
    """合并同一 sessionId 的两份记录（转录散落多文件时会出现）。

    以「调用更多」的那份为主档（信息更全），只从另一份补齐缺失字段并对列表型素材
    去重合并；`_human_turns` 取较大值而非求和 —— 同一段对话在两份文件里是重复的，
    相加会双计提问轮数。
    """
    keep, other = (a, b) if (a.get("_request_count") or 0) >= (b.get("_request_count") or 0) else (b, a)
    for field in ("cwd", "version", "model"):
        if not keep.get(field) and other.get(field):
            keep[field] = other[field]
    if not keep.get("created_at") and other.get("created_at"):
        keep["created_at"], keep["created_date"] = other["created_at"], other.get("created_date")
    keep["updated_at"] = max(_to_int(keep.get("updated_at")), _to_int(other.get("updated_at")))
    for lst in ("_skill_calls", "_presents"):
        seen = {tuple(x) for x in keep.get(lst) or []}
        merged = list(keep.get(lst) or [])
        for item in (other.get(lst) or []):
            if tuple(item) not in seen:
                seen.add(tuple(item))
                merged.append(item)
        keep[lst] = merged
    keep["_writes"] = sorted(set((keep.get("_writes") or []) + (other.get("_writes") or [])))
    keep["_human_turns"] = max(_to_int(keep.get("_human_turns")),
                              _to_int(other.get("_human_turns")))
    keep["_request_count"] = _to_int(keep.get("_request_count")) + _to_int(other.get("_request_count"))
    keep["_synthetic_responses"] = _to_int(keep.get("_synthetic_responses")) + \
        _to_int(other.get("_synthetic_responses"))
    keep["_merged_transcripts"] = _to_int(keep.get("_merged_transcripts")) + 1
    return keep


def _assemble(start_date, end_date, home=None, projects_root=None, db_path=None,
              use_run_logs=True):
    """解析候选会话并做 agents.db 增强，返回 (traces, sessions, extras)。

    extras 里是三个新维度的成品 + 供 `meta` 落盘的能力声明（渲染层读字段，
    不靠数据形态隐式猜）。
    """
    home = Path(home) if home else resolve_qwenwork_home()
    root = Path(projects_root) if projects_root else _projects_root(home)
    db_path = db_path or resolve_qwenwork_db(home)
    db_index = load_db_index(db_path)
    files = list(_iter_session_files(root, start_date, end_date, db_index))
    run_usage = {}
    if use_run_logs and files:
        run_usage = load_run_usage(home, {f.stem for f in files})
    traces = []
    sessions = {}
    # 跨文件去重：会话被恢复 / 续写时，同一个 sessionId 的行会散落在多个转录文件里，
    # 同一 requestId 的响应因此在两份文件中各存一份。不去重就会双计调用次数与 token
    # （本机月报实测：1022 条 trace 只有 834 个唯一 requestId，虚高 22%）。
    seen_requests = set()
    for f in files:
        file_traces, meta = _parse_session_file(f, start_date, end_date, run_usage)
        info = db_index.get(meta["id"]) or {}
        # agents.db 的标题是用户在界面上看到的真名，优先于首条提问截断
        if info.get("title"):
            meta["title"] = info["title"][:60]
        if info.get("cwd") and not meta.get("cwd"):
            meta["cwd"] = info["cwd"]
        if info.get("model_level"):
            meta["model"] = "%s:%s" % (QWENWORK_CHANNEL,
                                       normalize_model(info["model_level"]))
        if info.get("created_at") and not meta.get("created_at"):
            meta["created_at"] = _to_int(info["created_at"])
            meta["created_date"] = iso_to_date(_ms_to_iso(_to_int(info["created_at"])))
        if info.get("updated_at") and not meta.get("updated_at"):
            meta["updated_at"] = _to_int(info["updated_at"])
        meta["_db_duration_ms"] = _to_int(info.get("duration_ms"))
        meta["_db_num_turns"] = _to_int(info.get("num_turns"))

        uniq = []
        for t in file_traces:
            key = t.get("_request_id") or t["trace_id"]
            if key in seen_requests:
                continue
            seen_requests.add(key)
            uniq.append(t)
        traces.extend(uniq)

        prev = sessions.get(meta["id"])
        if prev is None:
            sessions[meta["id"]] = meta
        else:
            sessions[meta["id"]] = _merge_session(prev, meta)
    sessions = list(sessions.values())
    traces.sort(key=lambda x: x.get("ended_at") or "")

    active_days = {t["date"] for t in traces if t.get("date")}
    extras = {
        "skill_usage": aggregate_skill_usage(sessions, active_days),
        "outputs": collect_deliverables(sessions, start_date, end_date),
        "automation_runs": load_automation_runs(db_path, start_date, end_date),
        "meta": {
            "background_runs": load_background_runs(db_path, start_date, end_date),
            # 千问办公只有一层通道（档位即入口），§3.2「按入口/通道」必然与 §3.1 同构
            "single_channel": True,
            "skill_usage_source": "transcript:tool_use.Skill",
            "outputs_source": "transcript:present_files ∪ <cwd>/outputs",
        },
    }
    return traces, sessions, extras


def _finalize(sessions, extras=None):
    """预分类 task_type 并收口 db_data（与 codex / claude_code 适配器同结构 + 新维度）。"""
    extras = extras or {}
    out = []
    for s in sessions:
        text = s.get("_dialogue_text", "")
        s["task_type"] = classify_task(text)
        s.pop("_dialogue_text", None)
        out.append(s)
    return {"sessions": out,
            "automation_runs": extras.get("automation_runs") or [],
            "session_credits": [],
            "skill_usage": extras.get("skill_usage") or {"skills": {}, "active_days": []},
            "outputs": extras.get("outputs") or [],
            "_meta": extras.get("meta") or {}}


def collect_qwenwork_traces(start_date, end_date, home=None, projects_root=None,
                            db_path=None):
    """读取千问办公会话历史，返回统一 schema 的 trace 列表（token 为估算口径）。"""
    traces, _, _ = _assemble(start_date, end_date, home=home,
                             projects_root=projects_root, db_path=db_path)
    return traces


def collect_qwenwork_sessions(start_date, end_date, home=None, projects_root=None,
                              db_path=None):
    """读取千问办公会话历史，返回合成 db_data（sessions 已预分类 task_type）。"""
    _, sessions, extras = _assemble(start_date, end_date, home=home,
                                    projects_root=projects_root, db_path=db_path)
    return _finalize(sessions, extras)


def collect_qwenwork(start_date, end_date, home=None, projects_root=None, db_path=None):
    """一次性返回 (traces, db_data)，供 collect_usage_data.py --source qwenwork 使用。"""
    traces, sessions, extras = _assemble(start_date, end_date, home=home,
                                         projects_root=projects_root, db_path=db_path)
    return traces, _finalize(sessions, extras)
