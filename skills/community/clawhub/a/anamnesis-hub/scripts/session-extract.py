#!/usr/bin/env python3
"""
session-extract.py - 从历史会话中提取问题解决记忆

直接读取 sessions JSON + JSONL 文件 → memos-extractor 提取 → memos-reranker 去噪
→ 写入 .learnings/ERRORS.md + memory/YYYY-MM-DD.md

用法:
  python3 session-extract.py --days 5          # 最近5天
  python3 session-extract.py --full           # 全量首次运行
  python3 session-extract.py --dry-run         # 测试模式
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── 路径配置 ──────────────────────────────────────────────────────────────────

WORKSPACE = Path.home() / ".openclaw" / "workspace"
MEMORY_DIR = WORKSPACE / "memory"
LEARNINGS_DIR = WORKSPACE / ".learnings"
STATE_FILE = MEMORY_DIR / ".session-extract-state.json"

# 输出目标
ERRORS_FILE = LEARNINGS_DIR / "ERRORS.md"
LEARNINGS_FILE = LEARNINGS_DIR / "LEARNINGS.md"

# MemOS API
MEMOS_BASE_URL = "https://memos.memtensor.cn/api/openmem/v1"
MEMOS_API_KEY = ""

# 写入脚本
WRITER_SCRIPT = (
    WORKSPACE / "skills" / "cross-platform-writer" / "scripts" / "write_file.py"
)

# sessions 目录
SESSIONS_DIR = Path.home() / ".openclaw/agents/main/sessions"
SESSIONS_JSON = SESSIONS_DIR / "sessions.json"

# ── 当前会话识别 ──────────────────────────────────────────────────────────────

def get_current_session_id() -> str:
    """
    从 sessions.json 读取 agent:main:main 条目,
    返回当前活跃会话的 sessionId（如 6e5b9afc-6ea8-488b-98fe-201cc9b62fb3）。
    若读取失败返回空字符串。
    """
    try:
        if not SESSIONS_JSON.exists():
            return ""
        data = json.loads(SESSIONS_JSON.read_text(encoding="utf-8"))
        main_entry = data.get("agent:main:main", {})
        session_file = main_entry.get("sessionFile", "")
        if session_file:
            # sessionFile = /path/to/6e5b9afc-...jsonl → 提取 stem
            return Path(session_file).stem  # e.g. "6e5b9afc-6ea8-488b-98fe-201cc9b62fb3"
        return ""
    except Exception:
        return ""


# ── Reranker 配置 ──────────────────────────────────────────────────────────────

# 两个 query 串行去噪,保留通过任一 query 的条目
# 三路 query 串行去噪,保留通过任一 query 的条目（宽松 OR 逻辑）
QUERIES = [
    ("问题解决", "问题解决 错误修复 配置调试 方案决策 踩坑记录 报错解决 报错信息 修复方案 根本原因"),
    ("偏好经验", "偏好 习惯 用户喜欢 用户要求 决策 方案选择 操作流程 学习 经验 教训"),
    ("技术细节", "error message报错 账号密码 key配置 解决方案 步骤 命令 参数 报错信息 日志"),  # 新增: 覆盖报错/key/配置等 technical 内容
]

# 阈值调整（宽松）: 下调 main query 阈值,上调 meta 阈值防止误杀
THRESHOLD_PROBLEM = 0.15   # 0.30 → 0.15,保留更多问题解决类
THRESHOLD_PREF = 0.20      # 0.40 → 0.20,保留更多偏好经验类
THRESHOLD_TECH = 0.15      # 新增技术细节类阈值
THRESHOLD_PREF_META = 0.70 # 0.60 → 0.70,更宽松的元讨论过滤

# ── 工具函数 ──────────────────────────────────────────────────────────────────

def _get_memos_api_key() -> str:
    key = os.environ.get("MEMOS_API_KEY", "")
    if not key:
        env_path = Path.home() / ".openclaw" / ".env"
        if env_path.exists():
            for line in env_path.read_text().split("\n"):
                if line.startswith("MEMOS_API_KEY="):
                    key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return key


def call_extractor(messages: list) -> dict:
    """调用 memos-extractor-0.6b"""
    if not messages:
        return {"memory_detail_list": [], "preference_detail_list": []}

    payload = json.dumps({"messages": messages}).encode("utf-8")
    req = urllib.request.Request(
        f"{MEMOS_BASE_URL}/extract/memory",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {MEMOS_API_KEY}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("data", {}) or {}
    except urllib.error.HTTPError as e:
        if e.code == 400 and len(messages) > 5:
            # 400 可能因为 tokens 超限,尝试减半
            half = len(messages) // 2
            return call_extractor(messages[:half])
        print(f"[WARN] extractor: HTTP {e.code}", file=sys.stderr)
        return {"memory_detail_list": [], "preference_detail_list": []}
    except Exception as e:
        print(f"[WARN] extractor: {e}", file=sys.stderr)
        return {"memory_detail_list": [], "preference_detail_list": []}


def call_reranker(query: str, documents: list) -> list:
    """调用 memos-reranker,单 query"""
    if not documents:
        return []

    payload = {
        "model": "memos-reranker-0.6b",
        "query": query,
        "documents": documents,
    }
    req = urllib.request.Request(
        f"{MEMOS_BASE_URL}/rerank",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Token {MEMOS_API_KEY}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("data", {}).get("results", [])
    except Exception as e:
        print(f"[WARN] reranker: {e}", file=sys.stderr)
        return []


def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"version": 1, "lastRun": "", "processedIds": []}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


def write_with_script(path: str, content: str) -> dict:
    """直接写入文件(cross-platform-writer 用于生产环境,这里简化)"""
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(content, encoding="utf-8")
        return {"status": "ok", "path": path}
    except Exception as e:
        return {"status": "error", "message": str(e)}


# ── 会话读取 ──────────────────────────────────────────────────────────────────

def get_all_sessions(days: int = None, pass_num: int = 1) -> list:
    """
    直接扫描 sessions 目录的 .jsonl 文件（跳过 deleted 和 trajectory）,
    按 pass_num 过滤：
      pass=1: 只选 .jsonl（未分析）
      pass=2: 只选 .analyzed1.jsonl（已完成第一遍）
    读取每个文件内的 session 元数据，按 updatedAt 倒序返回。
    自动跳过最新会话（updatedAt 最高者），防止正在运行的会话被重命名。
    """
    sessions_dir = Path.home() / ".openclaw/agents/main/sessions"

    # 根据 pass 确定扩展名模式
    if pass_num == 1:
        pattern = "*.jsonl"
    else:
        pattern = "*.analyzed1"

    jsonl_files = list(sessions_dir.glob(pattern))
    sessions = []

    for jf in jsonl_files:
        full_stem = str(jf.name)

        if pass_num == 2 and full_stem.endswith(".analyzed1"):
            stem = full_stem[:-len(".analyzed1")]
            name = stem[:-len(".jsonl")] if stem.endswith(".jsonl") else stem
        else:
            name = jf.stem

        skip_patterns = ["deleted", "trajectory", "trajectory-path"]  # 明确跳过 trajectory-path.json
        if pass_num == 1:
            skip_patterns.extend(["analyzed1", "analyzed2"])
        if any(p in full_stem for p in skip_patterns):
            continue

        try:
            lines = jf.read_text(encoding="utf-8", errors="replace").splitlines()
        except Exception:
            continue

        updated_at = None
        session_key = None
        for line in lines:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") == "session":
                updated_at = obj.get("timestamp")
                session_key = obj.get("key")
                break

        if not updated_at:
            try:
                updated_at = jf.stat().st_mtime
                if updated_at > 1e12:
                    updated_at = updated_at / 1000
            except Exception:
                continue
        elif isinstance(updated_at, str):
            dt = datetime.fromisoformat(updated_at.replace("Z", "+00:00"))
            updated_at = dt.timestamp()
        elif isinstance(updated_at, (int, float)) and updated_at > 1e12:
            updated_at = updated_at / 1000

        # 时间过滤
        if days:
            cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).timestamp()
            if updated_at < cutoff:
                continue

        sessions.append({
            "sessionKey": session_key or name,
            "sessionId": name,
            "updatedAt": updated_at,
            "chatType": "unknown",
            "lastChannel": "",
            "filePath": jf,
        })

    sessions.sort(key=lambda x: x["updatedAt"], reverse=True)

    # pass=2 处理历史 analyzed1 文件，不应跳过最新会话
    if pass_num == 1 and sessions:
        latest_id = sessions[0]["sessionId"]
        print(f"[skip] 最新会话跳过: {latest_id}")
        sessions = sessions[2:]  # 跳过前2条：main(最新) + qqbot(次新)

    return sessions


def rename_session_file(session_file: Path, pass_num: int) -> bool:
    """将会话文件重命名标记。pass=1: .jsonl → .analyzed1.jsonl；pass=2: .analyzed1.jsonl → .analyzed2.jsonl"""
    try:
        if pass_num == 1:
            new_name = str(session_file) + ".analyzed1"
        else:
            # pass=2: xxx.analyzed1.jsonl → xxx.analyzed2.jsonl
            new_name = str(session_file) + ".analyzed2"
        session_file.rename(new_name)
        return True
    except Exception as e:
        print(f"[WARN] 重命名失败 {session_file.name}: {e}", file=sys.stderr)
        return False


def trash_session_file(session_file: Path) -> bool:
    """将会话文件移至系统回收站（gio trash）"""
    try:
        subprocess.run(["gio", "trash", str(session_file)], check=True, capture_output=True)
        print(f"[trash] 已移至回收站: {session_file.name}")
        return True
    except Exception as e:
        print(f"[WARN] 删除失败 {session_file.name}: {e}", file=sys.stderr)
        return False


def read_session_messages(session_id: str, session_key: str) -> list:
    """
    读取 .jsonl / .analyzed1.jsonl / .analyzed2.jsonl 文件，提取 user/assistant 对话消息，
    格式化为 extractor 所需的 messages 列表。
    """
    # 跳过 trajectory（推理日志，无对话内容）；checkpoint 包含完整对话，需要处理
    if "trajectory" in session_id:
        return []
    # checkpoint 文件名模式：xxx.checkpoint.xxx.jsonl（sessionId 包含 .checkpoint.）
    # 查找文件（支持普通 .jsonl、checkpoint、analyzed1/2）
    # 实际文件名格式：xxx.jsonl.analyzed1 / xxx.jsonl.analyzed2（不是 xxx.analyzed1.jsonl）
    sessions_dir = Path.home() / ".openclaw/agents/main/sessions"
    suffixes = [".analyzed1", ".analyzed2"]
    for suffix in suffixes:
        jsonl_path = sessions_dir / f"{session_id}.jsonl{suffix}"
        if jsonl_path.exists():
            break
    else:
        # 普通 .jsonl（无 suffix）
        jsonl_path = sessions_dir / f"{session_id}.jsonl"
        if not jsonl_path.exists():
            return []

    messages = []
    try:
        lines = jsonl_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as e:
        print(f"[WARN] 读取 {session_id} 失败: {e}", file=sys.stderr)
        return []

    for line in lines:
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue

        if obj.get("type") != "message":
            continue

        msg = obj.get("message", {})
        role = msg.get("role", "")
        if role not in ("user", "assistant"):
            continue

        content = msg.get("content", [])
        if isinstance(content, list):
            text_parts = []
            for part in content:
                if isinstance(part, dict) and part.get("type") == "text":
                    t = part.get("text", "").strip()
                    if t:
                        text_parts.append(t)
            text = "\n".join(text_parts)
        else:
            text = str(content).strip()

        if not text:
            continue

        # 剥离 Conversation info 元数据块（QQBot/TG 等渠道消息头）
        text = re.sub(
            r'Conversation info \(untrusted metadata\):\n```json\n[\s\S]*?\n```\n*',
            '',
            text,
            flags=re.MULTILINE
        )
        # 剥离纯系统消息（<!-- ... --> 整段）
        text = re.sub(r'^<!-- [\s\S]*?-->\s*$', '', text, flags=re.MULTILINE)
        text = text.strip()
        # 剥离后内容过短才跳过
        if len(text) < 20:
            continue

        # 截断超长消息（extractor 上限 8000 tokens）
        text = re.sub(r'```thinking[\s\S]*?```', '', text)
        text = re.sub(r'<thinking>[\s\S]*?</thinking>', '', text)
        if len(text) > 15000:
            text = text[:12000] + "\n...[truncated]..."

        messages.append({
            "role": role,
            "content": text,
        })

    return messages


def get_existing_hashes() -> set:
    """读取 ERRORS.md 和 LEARNINGS.md 中所有已有的条目哈希，用于第二遍查漏补缺"""
    hashes = set()
    for f in [ERRORS_FILE, LEARNINGS_FILE]:
        if f.exists():
            content = f.read_text(encoding="utf-8")
            for m in re.findall(r'<!-- learnings-import-hash:([a-f0-9]+) -->', content):
                hashes.add(m)
    return hashes


# ── 核心提取流程 ──────────────────────────────────────────────────────────────

def process_session(session_key: str, session_id: str, pass_num: int, dry_run: bool = False, existing_hashes: set = None) -> dict:
    """处理单个会话，pass_num 用于标记和去重"""
    messages = read_session_messages(session_id, session_key)
    if not messages:
        return {"sessionKey": session_key, "sessionId": session_id, "extracted": [], "skipped": True}

    if dry_run:
        return {
            "sessionKey": session_key,
            "sessionId": session_id,
            "messages_count": len(messages),
            "extracted": [],
            "skipped": False,
            "dry_run": True,
        }

    # extractor
    extracted = call_extractor(messages)
    memory_list = extracted.get("memory_detail_list", []) or []
    pref_list = extracted.get("preference_detail_list", []) or []

    if not memory_list and not pref_list:
        return {"sessionKey": session_key, "sessionId": session_id, "extracted": [], "skipped": True}

    # 收集 documents
    docs = []
    doc_sources = []
    for m in memory_list:
        val = m.get("memory_value", "") or ""
        key = m.get("memory_key", "") or ""
        if val:
            docs.append(f"{key}: {val}")
            doc_sources.append({"type": "memory", "data": m})

    for p in pref_list:
        pref = p.get("preference", "") or ""
        if pref:
            docs.append(pref)
            doc_sources.append({"type": "preference", "data": p})

    if not docs:
        return {"sessionKey": session_key, "sessionId": session_id, "extracted": [], "skipped": True}

    # 三 query 串行 reranker 去噪
    scores_p = call_reranker(QUERIES[0][1], docs)
    scores_e = call_reranker(QUERIES[1][1], docs)
    scores_m = call_reranker(QUERIES[2][1], docs)
    kept = []
    for i in range(len(docs)):
        sp = scores_p[i].get("relevance_score", 0) if i < len(scores_p) else 0
        se = scores_e[i].get("relevance_score", 0) if i < len(scores_e) else 0
        st = scores_m[i].get("relevance_score", 0) if i < len(scores_m) else 0  # 技术细节 score
        # 宽松 OR 逻辑: 任一主要 query 达标即保留,meta 过滤防止误杀
        # sm = scores_meta[i] 已移除; 用技术 query 阈值替代 meta 过滤逻辑
        if sp >= THRESHOLD_PROBLEM or se >= THRESHOLD_PREF or st >= THRESHOLD_TECH:
            src = doc_sources[i]
            # pass=2 时用哈希过滤已提取条目
            content_hash = hashlib.sha256(docs[i].encode()).hexdigest()[:16]
            if pass_num == 2 and existing_hashes and content_hash in existing_hashes:
                continue
            kept.append({
                "score": max(sp, se, st),
                "type": src["type"],
                "sessionKey": session_key,
                "sessionId": session_id,
                "content": docs[i],
                "raw": src["data"],
                "hash": content_hash,
            })

    return {
        "sessionKey": session_key,
        "sessionId": session_id,
        "extracted": kept,
        "total_in": len(docs),
        "kept_in": len(kept),
        "skipped": len(kept) == 0,
    }


# ── 写入 ──────────────────────────────────────────────────────────────────────

def append_to_errors(items: list, dry_run: bool = False):
    if not items:
        return

    ts = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
    marker = f"<!-- session-extract:{datetime.now().strftime('%Y-%m-%d')} -->"

    blocks = []
    for item in items:
        content = item["content"]
        score = item.get("score", 0)
        raw = item.get("raw", {})
        reasoning = raw.get("reasoning", "") or ""

        cat = "error_resolution" if any(k in content.lower() for k in ["error", "err", "报错", "失败", "修复", "解决"]) else "lesson_learned"

        blocks.append(f"""
### {ts} - [{cat}] (score={score:.2f})

**来源会话**: {item['sessionKey']}
**内容**: {content}
**推断依据**: {reasoning}
""")

    new_block = f"\n{marker}\n" + "\n".join(blocks) + "\n"

    LEARNINGS_DIR.mkdir(parents=True, exist_ok=True)
    if ERRORS_FILE.exists():
        existing = ERRORS_FILE.read_text(encoding="utf-8")
    else:
        existing = "# ERRORS.md - 错误与教训记录\n\n记录 Agent 在会话中遇到的技术错误、修复方案和经验教训。\n\n"

    existing = existing.rstrip() + "\n" + new_block

    if dry_run:
        print(f"[DRY RUN] 会写入 ERRORS.md: {len(items)} 条")
        return

    write_with_script(str(ERRORS_FILE), existing)
    print(f"[ERRORS.md] 写入 {len(items)} 条")


def append_to_learnings(items: list, dry_run: bool = False):
    """写入 LEARNINGS.md(非 error 类条目)"""
    non_error = [
        it for it in items
        if not any(k in it["content"].lower() for k in ["error", "err", "报错", "失败"])
    ]
    if not non_error:
        return

    ts = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
    marker = f"<!-- session-extract:{datetime.now().strftime('%Y-%m-%d')} -->"

    blocks = []
    for item in non_error:
        content = item["content"]
        score = item.get("score", 0)
        raw = item.get("raw", {})
        reasoning = raw.get("reasoning", "") or ""

        blocks.append(f"""
### {ts} - [lesson_learned] (score={score:.2f})

**来源会话**: {item['sessionKey']}
**内容**: {content}
**推断依据**: {reasoning}
""")

    new_block = f"\n{marker}\n" + "\n".join(blocks) + "\n"

    if LEARNINGS_FILE.exists():
        existing = LEARNINGS_FILE.read_text(encoding="utf-8")
    else:
        existing = "# LEARNINGS.md - 经验教训记录\n\n记录从会话中提取的教训、经验和方法论。\n\n"

    existing = existing.rstrip() + "\n" + new_block

    if dry_run:
        print(f"[DRY RUN] 会写入 LEARNINGS.md: {len(non_error)} 条")
        return

    write_with_script(str(LEARNINGS_FILE), existing)
    print(f"[LEARNINGS.md] 写入 {len(non_error)} 条")


def append_to_memory(error_items: list, lesson_items: list, dry_run: bool = False):
    """
    将 session-extract 提取的记忆追加写入 memory/YYYY-MM-DD.md。
    被 sync-all.sh 自动处理:Cloud 同步 + 向量索引 + Dreaming 评估。
    """
    from hashlib import sha256

    today = datetime.now().strftime("%Y-%m-%d")
    MEMORY_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / f"{today}.md"

    # 构建条目哈希集合用于去重
    new_entries = []
    for it in error_items:
        h = sha256(it["content"].encode()).hexdigest()[:16]
        new_entries.append({
            "type": "error",
            "content": it["content"],
            "score": it.get("score", 0),
            "session": it.get("sessionKey", it.get("sessionId", ""))[:40],
            "hash": h,
        })
    for it in lesson_items:
        h = sha256(it["content"].encode()).hexdigest()[:16]
        new_entries.append({
            "type": "lesson",
            "content": it["content"],
            "score": it.get("score", 0),
            "session": it.get("sessionKey", it.get("sessionId", ""))[:40],
            "hash": h,
        })

    if not new_entries:
        return {"imported": 0}

    # 读取已有文件的哈希集合
    existing_hashes = set()
    if MEMORY_FILE.exists():
        existing = MEMORY_FILE.read_text(encoding="utf-8")
        import re
        for m in re.findall(r"<!-- learnings-import-hash:([a-f0-9]+) -->", existing):
            existing_hashes.add(m)

    # 过滤已存在的
    to_import = [e for e in new_entries if e["hash"] not in existing_hashes]
    if not to_import:
        print("[memory] 无新条目需导入")
        return {"imported": 0}

    error_count = sum(1 for e in to_import if e["type"] == "error")
    lesson_count = sum(1 for e in to_import if e["type"] == "lesson")

    ts = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M")
    lines = []
    lines.append("")
    lines.append(f"## learnings-import [session-extract]")
    lines.append("")
    if error_count:
        lines.append(f"### 从 ERRORS.md 导入({error_count} 条)")
        lines.append(f"<!-- learnings-import:error:{today} -->")
        for e in to_import:
            if e["type"] == "error":
                lines.append(f"- **[error_resolution]** [session:{e['session']}] {e['content']} (score={e['score']:.2f}) <!-- learnings-import-hash:{e['hash']} -->")
        lines.append("")
    if lesson_count:
        lines.append(f"### 从 LEARNINGS.md 导入({lesson_count} 条)")
        lines.append(f"<!-- learnings-import:lesson:{today} -->")
        for e in to_import:
            if e["type"] == "lesson":
                lines.append(f"- **[lesson_learned]** [session:{e['session']}] {e['content']} (score={e['score']:.2f}) <!-- learnings-import-hash:{e['hash']} -->")
        lines.append("")

    new_block = "\n".join(lines)

    if dry_run:
        print(f"[DRY RUN] 会写入 memory/{today}.md: {len(to_import)} 条")
        return {"imported": 0, "dry_run": True}

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    existing = MEMORY_FILE.read_text(encoding="utf-8") if MEMORY_FILE.exists() else ""
    existing = existing.rstrip() + "\n" + new_block
    MEMORY_FILE.write_text(existing, encoding="utf-8")
    print(f"[memory] 写入 {len(to_import)} 条 → memory/{today}.md")
    return {"imported": len(to_import)}



# ── 主流程 ────────────────────────────────────────────────────────────────────

def run_full(days: int = None, dry_run: bool = False, pass_num: int = 1) -> dict:
    """
    全量处理所有会话，不限数量。
    pass=1: .jsonl → .analyzed1.jsonl
    pass=2: .analyzed1.jsonl → .analyzed2.jsonl → gio trash
    """
    global MEMOS_API_KEY
    MEMOS_API_KEY = _get_memos_api_key()
    if not MEMOS_API_KEY:
        return {"status": "error", "message": "MEMOS_API_KEY 未配置"}

    print(f"[session-extract] 开始 (days={days or '全量'}, pass={pass_num}, dry_run={dry_run})")

    sessions = get_all_sessions(days=days, pass_num=pass_num)
    if not sessions:
        print(f"[session-extract] pass={pass_num} 未找到待处理文件")
        return {"status": "ok", "message": f"pass={pass_num} 无待处理文件"}

    print(f"[session-extract] 获取到 {len(sessions)} 个会话 (pass={pass_num})")

    state = load_state()
    processed = set(state.get("processedIds", []))
    today_str = datetime.now().strftime("%Y-%m-%d")

    # pass=2 时读取已有哈希用于去重
    existing_hashes = get_existing_hashes() if pass_num == 2 else None

    all_items = []
    session_count = 0
    skip_count = 0
    rename_count = 0
    trash_count = 0

    for sess in sessions:
        session_key = sess["sessionKey"]
        session_id = sess["sessionId"]
        session_file = sess.get("filePath")
        if not session_id:
            continue

        if not dry_run and session_id in processed:
            continue

        session_count += 1
        print(f"[{session_count}] {session_key[:55]}...", end=" ", flush=True)

        result = process_session(session_key, session_id, pass_num, dry_run=dry_run, existing_hashes=existing_hashes)
        items = result.get("extracted", [])

        if items:
            all_items.extend(items)
            print(f"✓ {len(items)} 条保留 ({result.get('total_in',0)}→{len(items)})")
        else:
            skip_count += 1
            print(f"○ 无相关记忆")

        # 标记 / 归档文件（跳过 dry_run）
        if not dry_run and session_file and session_file.exists():
            if pass_num == 1:
                if rename_session_file(session_file, pass_num):
                    rename_count += 1
            elif pass_num == 2:
                # 重命名为 analyzed2 后即移至回收站
                if rename_session_file(session_file, pass_num):
                    # 找到新的 .analyzed2.jsonl 文件
                    new_path = Path(str(session_file) + ".analyzed2")
                    if new_path.exists():
                        trash_session_file(new_path)
                        trash_count += 1

        if not dry_run:
            processed.add(session_id)
            state["processedIds"] = list(processed)
            state["lastRun"] = today_str
            state["lastPass"] = pass_num
            save_state(state)

        time.sleep(0.5)

    print(f"\n[完成] pass={pass_num} 处理 {session_count} 会话, {len(all_items)} 条有效记忆, {skip_count} 条跳过")
    print(f"[文件] 重命名 {rename_count} 个, 移至回收站 {trash_count} 个")

    if dry_run:
        return {"status": "dry_run", "session_count": session_count, "total_kept": len(all_items)}

    if not all_items:
        return {"status": "ok", "message": "无相关记忆", "skipped": True}

    error_items = [it for it in all_items if any(k in it["content"].lower() for k in ["error", "err", "报错", "失败", "修复", "解决"])]
    lesson_items = [it for it in all_items if it not in error_items]

    append_to_errors(error_items)
    append_to_learnings(lesson_items)

    # 追加写入 memory/，供 sync-all.sh 自动处理
    mem_result = append_to_memory(error_items, lesson_items, dry_run=dry_run)

    return {
        "status": "ok",
        "pass": pass_num,
        "session_count": session_count,
        "total_kept": len(all_items),
        "errors_count": len(error_items),
        "learnings_count": len(lesson_items),
        "memory_imported": mem_result.get("imported", 0),
        "files_renamed": rename_count,
        "files_trashed": trash_count,
    }


def cleanup_trashable_files(dry_run: bool = False) -> dict:
    """
    提取完成后清理sessions目录中的无用文件。
    保护：当前会话 + QQBot会话 + sessions.json
    可回收：trajectory / trajectory-path / analyzed1 / reset / deleted
    """
    sessions_dir = Path.home() / ".openclaw/agents/main/sessions"
    current_id = get_current_session_id()

    # 从 sessions.json 读取 QQBot 当前会话 ID
    qqbot_session_id = None
    try:
        data = json.loads((sessions_dir / "sessions.json").read_text())
        qqbot_entry = data.get("agent:main:qqbot:direct:0a39eb9443f8c5bc34b129d50deb747e", {})
        sf = qqbot_entry.get("sessionFile", "")
        if sf:
            qqbot_session_id = Path(sf).stem  # e.g. "c4e539d2-3c6c-43e8-9629-9ceb2d4e548c"
    except Exception:
        pass

    protected = {current_id, qqbot_session_id}.difference({"", None})
    print(f"[cleanup] 保护会话: {protected}")

    categories = {
        "trajectory": [],
        "trajectory_path": [],
        "analyzed1": [],
        "reset": [],
        "deleted": [],
    }

    for f in sessions_dir.iterdir():
        if f.is_dir() or f.name == "sessions.json" or f.name == "sessions.json.bak.20260512":
            continue
        bn = f.name
        sid = bn.replace(".jsonl", "").replace(".json", "")

        if bn in protected or sid in protected:
            continue

        if ".trajectory.jsonl" in bn:
            categories["trajectory"].append(f)
        elif ".trajectory-path.json" in bn:
            categories["trajectory_path"].append(f)
        elif ".analyzed1" in bn:
            categories["analyzed1"].append(f)
        elif ".jsonl.reset." in bn:
            categories["reset"].append(f)
        elif ".deleted." in bn:
            categories["deleted"].append(f)

    if dry_run:
        for cat, files in categories.items():
            print(f"[DRY RUN] {cat}: {len(files)} 个可回收")
        return {cat: len(files) for cat, files in categories.items()}

    total = 0
    for cat, files in categories.items():
        for f in files:
            if trash_session_file(f):
                total += 1

    return {"trashed": total, "categories": {cat: len(files) for cat, files in categories.items()}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=None, help="拉取最近N天")
    parser.add_argument("--full", action="store_true", help="全量（等同于 pass=1）")
    parser.add_argument("--dry-run", action="store_true", help="测试模式")
    parser.add_argument("--reset", action="store_true", help="重置处理状态，重新全量运行")
    parser.add_argument("--pass-num", type=int, default=1, choices=[1, 2], help="分析遍次：1=首次全量，2=查漏补缺（默认1）")
    parser.add_argument("--cleanup", action="store_true", help="提取完成后清理可回收文件（trajectory/analyzed1/reset/deleted 等）")
    args = parser.parse_args()

    # --reset 时清除 processed 状态，重新全量运行
    if args.reset:
        state = load_state()
        if state.get("processedIds"):
            print(f"[RESET] 清除 {len(state['processedIds'])} 条处理记录")
            state["processedIds"] = []
            save_state(state)

    pass_num = args.pass_num
    if pass_num not in (1, 2):
        print("[ERROR] pass 必须是 1 或 2")
        return 1
    days = None if args.full else (args.days or 5)
    result = run_full(days=days, dry_run=args.dry_run, pass_num=pass_num)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 提取完成后自动清理可回收文件
    if args.cleanup and result.get("status") == "ok" and not args.dry_run:
        print("\n[cleanup] 开始清理可回收文件...")
        cleanup_result = cleanup_trashable_files(dry_run=False)
        print(f"[cleanup] 已回收 {cleanup_result.get('trashed', 0)} 个文件:")
        for cat, cnt in cleanup_result.get("categories", {}).items():
            if cnt:
                print(f"  {cat}: {cnt}")

    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
