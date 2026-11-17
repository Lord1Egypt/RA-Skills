#!/usr/bin/env python3
"""ai-content-guard 统一入口 — AI 内容安检（PITAX 确定性引擎 + 信封输出）。

架构宪法（docs/design-decisions.md）：
  1. 判决权归引擎：verdict/counts/去重/脱敏全部由本脚本确定性产出，模型只解释；
  2. 三层输出：聊天只回紧凑信封（≤8k），完整 findings 落 report.jsonl，人读摘要 summary.md；
  3. 注入防御：脚本预脱敏——被检内容的原文永不进入模型上下文。

铁律：纯标准库 / 零网络 / 只读扫描 / 永不执行被检内容 / 失败返回结构化错误。

用法：
    python entry.py --text "粘贴的邮件/消息/文档内容"
    python entry.py --file "C:\\path\\to\\可疑文件.md"     （--file - 读 stdin）
    python entry.py --dir  "C:\\path\\to\\repo"             （--mode config 只审 AI 配置文件）
    python entry.py --decode "SGVsbG8..."                   （编码载荷分层复核，≤3 层）
    python entry.py --self-check                            （边界自证：网络/写盘/动态执行/规则哈希）

退出码：0=完成；1=--fail-on 命中；2=参数错误；3=运行时错误。
"""
from __future__ import annotations

import argparse
import base64
import binascii
import fnmatch
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from pathlib import PurePosixPath as pathlib_posix

sys.dont_write_bytecode = True  # 安装副本不留 __pycache__（P2-9）

# ── 编码三件套（第 1 件）：天禧自带 Python 3.14 的控制台默认 GBK，先改 UTF-8 ──
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

_SCRIPT_DIR = Path(__file__).resolve().parent
if str(_SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPT_DIR))

from engine.detectors import is_ai_config_path  # noqa: E402
from engine.rules import ALL_RULES, PITAX_VERSION  # noqa: E402
from engine.sanitizer import MAX_FILE_BYTES, SCAN_EXTENSIONS, SKIP_DIRS  # noqa: E402
from engine.sarif import build_sarif  # noqa: E402
from engine.scan import scan_file, scan_repo  # noqa: E402

SKILL_NAME = "ai-content-guard"
SKILL_VERSION = "1.3.3"
SCHEMA_VERSION = "1.0"

# ── 扫描防护上限（对齐 docs/design-decisions.md 八条）──
DEFAULT_MAX_FILES = 5000
DEFAULT_MAX_BYTES = 200 * 1024 * 1024
DEFAULT_MAX_DEPTH = 20
DEFAULT_TIMEOUT_S = 30

_SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}

# 系统目录拒绝清单（realpath 后按路径隶属判断，绝不做字符串前缀匹配）
_SYSTEM_DIRS = [
    Path(os.environ.get("WINDIR", r"C:\Windows")),
    Path(r"C:\Program Files"), Path(r"C:\Program Files (x86)"),
    Path(r"C:\ProgramData"),
    Path("/etc"), Path("/usr"), Path("/bin"), Path("/sbin"),
    Path("/System"), Path("/Library"), Path("/private"), Path("/var"),
]

# 敏感文件：只报存在，绝不读内容、不展示内容
_SENSITIVE_PATTERNS = [
    ".env", ".env.*", "*.env", "*.pem", "*.key", "id_rsa*", "id_ed25519*",
    "credentials*", "cookies*", "Login Data", "*.sqlite", "*.db",
    "NTDS.dit", "SAM", "SECURITY", "*.kdbx", "*.pfx", "*.p12", "*.wallet",
]
# 注：`*.env` 覆盖 secret.env / prod.env 等任意命名（2026-11-08 ClawHub 扫描 C 项 #14：
# 原名单只有 `.env`/`.env.*`，`secret.env` 会被当普通文本读取）

# 产品级跳过目录：比引擎管线口径更窄——dist/build/node_modules 属分发内容，
# 对内容安检恰好是攻击者藏身处（复测 §3.4），必须扫；只跳 VCS 内部与缓存。
SKILL_SKIP_DIRS = SKIP_DIRS - {"node_modules", "dist", "build"}
# 贴入文本的多路由虚拟名：同一内容走"文档路径(N-06)"与"代码路径(4 检测器)"两趟；
# 另抽 base64 候选串构造带引号的虚拟代码行——引擎编码检测只认字符串字面量
# （防误报设计），裸文本中的编码载荷须经此适配才能进入剥离链。
_TEXT_VIRTUAL_NAMES = ["pasted-content.md", "pasted-content.py"]
_B64_RUN_RE = re.compile(r"[A-Za-z0-9+/]{24,}={0,2}")
_MAX_PAYLOAD_CANDIDATES = 64

_BINARY_SNIFF_BYTES = 8192
_DECODE_CHAIN = ("utf-8-sig", "utf-8", "gb18030", "utf-16")

# 零宽/双向控制符（输出时以 U+XXXX 记法呈现，原字符不进任何输出）
_INVISIBLE_RE = re.compile("[\u200b\u200c\u200d\u2060\ufeff\u202a-\u202e\u00ad]")
_LONG_TOKEN_RE = re.compile(r"[A-Za-z0-9+/=]{40,}")
_B64_CANDIDATE_RE = re.compile(r"^[A-Za-z0-9+/]{16,}={0,2}$")
# 密钥模式（P0-4）：短密钥不吃 40+ 长度线，必须单独脱敏
_KEY_PATTERNS = re.compile(
    r"(sk-[A-Za-z0-9_-]{6,}|AKIA[0-9A-Z]{12,}|ghp_[A-Za-z0-9]{10,}|gho_[A-Za-z0-9]{10,}"
    r"|xox[baprs]-[A-Za-z0-9-]{6,}|Bearer\s+[A-Za-z0-9._-]{8,}"
    r"|(?:api[_-]?key|apikey|secret|token|passwd|password)\s*[=:]\s*[\"\']?[A-Za-z0-9._-]{6,})",
    re.I)


def _mask_secrets(text: str) -> str:
    def _m(m: re.Match) -> str:
        s = m.group(0)
        return s[:4] + "****" + s[-4:] if len(s) > 12 else s[:2] + "****"
    return _KEY_PATTERNS.sub(_m, text)


# ══════════════════════ 基础工具 ══════════════════════

def _decode_bytes(data: bytes) -> str:
    """编码三件套（第 3 件）：文件/stdin 按链解码，全部失败则替换解码。"""
    for enc in _DECODE_CHAIN:
        try:
            return data.decode(enc)
        except (UnicodeDecodeError, LookupError):
            continue
    return data.decode("utf-8", errors="replace")


def _sha8(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()[:8]


def _is_under(p: Path, root: Path) -> bool:
    try:
        p.relative_to(root)
        return True
    except ValueError:
        return False


def guard_root(raw: str) -> Path:
    """防护①：规范化 + 系统目录拒绝。"""
    root = Path(raw).expanduser().resolve()
    for d in _SYSTEM_DIRS:
        try:
            if _is_under(root, d.expanduser().resolve()):
                raise ValueError(f"拒绝扫描系统目录：{root}")
        except OSError:
            continue
    return root


def _is_sensitive(rel: str) -> bool:
    name = rel.replace("\\", "/").rsplit("/", 1)[-1].lower()
    return any(fnmatch.fnmatch(name, pat.lower()) for pat in _SENSITIVE_PATTERNS)


def _is_reparse(entry) -> bool:
    """防护②：符号链接与 Windows junction/reparse point 都不跟随。"""
    if entry.is_symlink():
        return True
    try:
        return bool(entry.stat(follow_symlinks=False).st_file_attributes & 0x400)
    except (AttributeError, OSError):
        return False


# ══════════════════════ 输入采集 ══════════════════════

def _read_file_bytes(path: Path) -> bytes:
    """防护⑤/⑥：只读打开 + BOM 感知的二进制嗅探（UTF-16 不误判）+ 单文件上限。"""
    if path.stat().st_size > MAX_FILE_BYTES:
        raise ValueError(f"文件超过单文件上限（{MAX_FILE_BYTES // 1024}KB）：{path}")
    with open(path, "rb") as fh:  # noqa: SIM115 - 显式只读
        data = head = fh.read(_BINARY_SNIFF_BYTES)
        if len(head) == _BINARY_SNIFF_BYTES:
            data = head + fh.read()
    # UTF-16/UTF-32 BOM 优先：其 NUL 字节是编码字节而非二进制标志
    if data[:2] in (b"\xff\xfe", b"\xfe\xff") or data[:4] in (b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff"):
        return data
    if b"\x00" in data[:_BINARY_SNIFF_BYTES]:
        raise ValueError(f"二进制文件，跳过：{path.name}")
    return data


def _guard_file(fpath: Path) -> None:
    """file mode 防护（P0-3）：系统目录拒绝 + 敏感文件拒绝 + 符号链接不跟随，与 dir mode 同口径。"""
    # 防护②：先于 resolve() 检查符号链接（ClawHub 扫描 C 项 #37：resolve 会跟随链接，
    # 之后的检查落在链接目标上，原始链接信息丢失=no-follow 文档承诺失效）
    if fpath.is_symlink():
        raise ValueError(f"符号链接不跟随（file mode）：{fpath}")
    resolved = fpath.resolve()
    if resolved != fpath.absolute() and resolved.is_symlink():
        raise ValueError(f"符号链接不跟随（file mode）：{fpath}")
    for d in _SYSTEM_DIRS:
        try:
            if _is_under(resolved, d.expanduser().resolve()):
                raise ValueError(f"拒绝读取系统目录内文件：{resolved}")
        except OSError:
            continue
    if _is_sensitive(fpath.name):
        raise ValueError(f"敏感文件只报存在、不读取内容：{fpath.name}")


def collect_dir(root: Path, max_files: int, max_bytes: int,
                max_depth: int, timeout_s: int, config_only: bool = False):
    """目录采集：八条防护中的①②③④⑥⑧在此落地。返回 (files, coverage, errors)。"""
    files: dict[str, str] = {}
    errors: list[str] = []
    coverage = {
        "root": str(root), "files_scanned": 0, "files_skipped": 0,
        "dirs_skipped": 0, "dirs_skipped_names": [],
        "sensitive_skipped": [], "bytes_scanned": 0, "truncated": False,
        "limits": ["确定性层仅覆盖 PITAX 规则集；语义改写类攻击不在本层覆盖内"],
    }
    deadline = time.monotonic() + timeout_s
    stopped = None

    def walk(dir_path: Path, depth: int) -> None:
        nonlocal stopped
        if depth > max_depth:
            if not coverage["truncated"]:
                coverage["truncated"] = True
                coverage["limits"].append(f"超过 max-depth={max_depth}，深层目录未扫")
            return
        try:
            entries = sorted(os.scandir(dir_path), key=lambda e: e.name)
        except (PermissionError, OSError) as exc:
            errors.append(f"目录不可读（{type(exc).__name__}）：{dir_path}")
            return
        for entry in entries:
            if stopped:
                return
            if time.monotonic() >= deadline:  # >= ：Windows 计时器粒度下相同 tick 也要停
                stopped = "timeout"
                coverage["truncated"] = True
                coverage["limits"].append(f"达到 {timeout_s}s 超时上限，未扫完")
                return
            if entry.is_dir(follow_symlinks=False):
                if _is_reparse(entry):
                    coverage["links_skipped"] = coverage.get("links_skipped", 0) + 1
                    if len(coverage.get("links_skipped_names", [])) < 10:
                        coverage.setdefault("links_skipped_names", []).append(entry.name)
                    continue
                if entry.name in SKILL_SKIP_DIRS:
                    coverage["dirs_skipped"] = coverage.get("dirs_skipped", 0) + 1
                    if len(coverage.get("dirs_skipped_names", [])) < 10:
                        coverage.setdefault("dirs_skipped_names", []).append(entry.name)
                    continue
                if _is_reparse(entry):
                    continue
                walk(Path(entry.path), depth + 1)
                continue
            if not entry.is_file(follow_symlinks=False) or _is_reparse(entry):
                if _is_reparse(entry):
                    coverage["links_skipped"] = coverage.get("links_skipped", 0) + 1
                    if len(coverage.get("links_skipped_names", [])) < 10:
                        coverage.setdefault("links_skipped_names", []).append(entry.name)
                continue
            rel = str(Path(entry.path).relative_to(root)).replace("\\", "/")
            if _is_sensitive(rel):  # 防护③：敏感文件只报存在
                if len(coverage["sensitive_skipped"]) < 20:
                    coverage["sensitive_skipped"].append(rel)
                coverage["files_skipped"] += 1
                continue
            if config_only and not is_ai_config_path(rel):
                continue
            try:
                if entry.stat(follow_symlinks=False).st_size > MAX_FILE_BYTES:
                    coverage["files_skipped"] += 1
                    continue
                data = _read_file_bytes(Path(entry.path))
            except ValueError as exc:
                coverage["files_skipped"] += 1
                if "二进制" not in str(exc):
                    errors.append(str(exc))
                continue
            except (PermissionError, OSError) as exc:
                errors.append(f"文件不可读（{type(exc).__name__}）：{rel}")  # 防护⑧
                coverage["files_skipped"] += 1
                continue
            if len(files) >= max_files or coverage["bytes_scanned"] + len(data) > max_bytes:
                stopped = "caps"
                coverage["truncated"] = True
                coverage["limits"].append(
                    f"达到 max-files={max_files} / max-bytes={max_bytes // (1024 * 1024)}MB 上限，未扫完")
                return
            files[rel] = _decode_bytes(data)
            coverage["files_scanned"] += 1
            coverage["bytes_scanned"] += len(data)

    walk(root, 0)
    return files, coverage, errors


def collect_text(text: str):
    """贴入文本：同一内容按多路由虚拟名扫描，命中去重。"""
    seen: set[tuple] = set()
    findings: list[dict] = []
    for virtual in _TEXT_VIRTUAL_NAMES:
        for f in scan_file(virtual, text, _n=1):
            key = (f.get("type"), f.get("line"), (f.get("code_snippet") or "")[:120])
            if key in seen:
                continue
            seen.add(key)
            f = dict(f)
            f["file"] = "<粘贴内容>"
            findings.append(f)
    # 编码载荷适配：base64 候选串 → 带引号虚拟代码行 → 引擎剥离链（E-07/14/36/57）
    candidates = _B64_RUN_RE.findall(text)[:_MAX_PAYLOAD_CANDIDATES]
    if candidates:
        virtual_code = "\n".join('payload = "%s"' % b for b in candidates)
        for f in scan_file("pasted-payloads.py", virtual_code, _n=1):
            key = (f.get("type"), "enc", (f.get("code_snippet") or "")[:120])
            if key in seen:
                continue
            seen.add(key)
            f = dict(f)
            f["file"] = "<粘贴内容·编码载荷>"
            findings.append(f)
    coverage = {
        "root": "<粘贴文本>", "files_scanned": 1, "files_skipped": 0,
        "dirs_skipped": 0, "dirs_skipped_names": [],
        "sensitive_skipped": [], "bytes_scanned": len(text.encode("utf-8", errors="replace")),
        "truncated": False,
        "limits": ["确定性层仅覆盖 PITAX 规则集；语义改写类攻击不在本层覆盖内"],
    }
    return _post_filter(findings), coverage, []


# ══════════════════════ 脱敏（架构宪法③：原文不进模型上下文）══════════════════════

def _notation_invisible(text: str) -> str:
    return _INVISIBLE_RE.sub(
        lambda m: "‹U+%04X›" % ord(m.group(0)), text)


def redact_fragment(raw: str, limit: int = 40) -> str:
    """按 F6 规范脱敏：密钥模式掩码 + 隐形字符记法化 + 长编码串取前后缀 + 截断。"""
    out = _mask_secrets(_notation_invisible(raw))
    out = _LONG_TOKEN_RE.sub(lambda m: m.group(0)[:8] + "…" + m.group(0)[-8:], out)
    out = out.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")
    return out[:limit]


def _teaser(raw: str) -> str:
    """零原文口径：片段只留前 4+后 4 字符（过密钥掩码与不可见记法之后），
    拼接出的内容不足以复原任何可执行注入指令。"""
    s = _mask_secrets(_notation_invisible(raw))
    if len(s) <= 12:
        return s[:2] + "…"
    return s[:4] + "…" + s[-4:]


def _scrub_description(desc: str, evidence: str) -> str:
    """叙述字段零原文：把 description 中出现的证据原文（及其前 30 字符）替换掉。"""
    if not evidence:
        return desc
    out = desc.replace(evidence, "[证据已脱敏]")
    head = evidence[:30]
    if len(head) >= 12 and head in out:
        out = out.replace(head, "[证据已脱敏]")
    return out


def redact_finding(f: dict) -> dict:
    """输出前逐条脱敏（零原文口径）：证据只保留 记法+长度+SHA8+前后4字符 teaser；
    解码载荷只留 长度+SHA8；description 叙述字段洗掉证据原文。"""
    raw_ev = (f.get("code_snippet") or "")[:240]
    evidence = _mask_secrets(raw_ev)
    pitax = f.get("pitax") if isinstance(f.get("pitax"), dict) else {}
    decoded = pitax.get("decoded_payload")
    red = {
        "id": f.get("id"),
        "type": f.get("type"),
        "severity": f.get("severity"),
        "confidence": f.get("confidence"),
        "title": f.get("title"),
        "file": f.get("file"),
        "line": f.get("line"),
        "evidence_redacted": "[{code}] len={len} sha={sha} frag={frag}".format(
            code=f.get("type"), len=len(evidence), sha=_sha8(evidence),
            frag=_teaser(raw_ev)),
        "description": _scrub_description(str(f.get("description") or ""), raw_ev),
        "advice": f.get("suggestion"),
    }
    if decoded:
        dec = _mask_secrets(str(decoded))
        red["decoded_redacted"] = "[decoded] len={len} sha={sha}".format(
            len=len(dec), sha=_sha8(dec))
    return red


# ══════════════════════ 四值判决聚合 ══════════════════════

def _dedup(findings: list[dict]) -> list[dict]:
    """引擎+覆盖层双路径产生的同命中去重（type+file+line+证据前缀为键），
    统一重编号（修 counts 虚高与重复 ID）。"""
    seen: set = set()
    out: list[dict] = []
    for f in findings:
        key = (f.get("type"), str(f.get("file")), f.get("line"),
               (f.get("code_snippet") or "")[:120])
        if key in seen:
            continue
        seen.add(key)
        out.append(f)
    for i, f in enumerate(out, start=1):
        f["id"] = f"F{i}"
    return out


def _post_filter(findings: list[dict]) -> list[dict]:
    """emoji 家族序列误报降级：U+200D 两侧均为 emoji 类字符时，E-23 降为 low。"""
    def _emojiish(ch: str) -> bool:
        o = ord(ch)
        return 0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF or 0x2190 <= o <= 0x21FF \
            or 0x2B00 <= o <= 0x2BFF or ch in "️⃝"

    for f in findings:
        if f.get("type") != "PIT-E-23":
            continue
        snip = f.get("code_snippet") or ""
        positions = [i for i, c in enumerate(snip) if c == "\u200d"]
        if positions and all(
            (i > 0 and _emojiish(snip[i - 1])) and (i + 1 < len(snip) and _emojiish(snip[i + 1]))
            for i in positions
        ):
            f["severity"] = "low"
            f["description"] = (str(f.get("description", "")) +
                                "（该 ZWJ 位于 emoji 家族序列内部，已降级为低风险）").strip()
    return findings


def aggregate(findings: list[dict], coverage: dict, errors: list[str]) -> dict:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
    for f in findings:
        counts[str(f.get("severity", "info")).lower()] = counts.get(
            str(f.get("severity", "info")).lower(), 0) + 1
    if counts["critical"] or counts["high"]:
        verdict, confidence = "malicious", 0.9
    elif counts["medium"]:
        verdict, confidence = "suspicious", 0.7
    elif errors or coverage.get("truncated"):
        verdict, confidence = "inconclusive", 0.3
        if errors:
            coverage["limits"].append(f"扫描过程 {len(errors)} 项错误，覆盖不完整")
    else:
        # clean 不过度自信：确定性层覆盖有限（规则集/路由），0.6 而非 0.9
        verdict, confidence = "clean", 0.6
    return {"verdict": verdict, "verdict_source": "engine",
            "confidence": confidence, "counts": counts}


# ══════════════════════ 输出三件套 ══════════════════════

def _risk_word(verdict: str) -> str:
    return {"malicious": "高风险", "suspicious": "可疑",
            "clean": "未检出", "inconclusive": "无法完成"}.get(verdict, verdict)


def build_summary_text(agg: dict, coverage: dict) -> str:
    c = agg["counts"]
    hot = c["critical"] + c["high"]
    if agg["verdict"] == "malicious":
        head = f"检出 {hot} 项高危（critical {c['critical']} / high {c['high']}）"
    elif agg["verdict"] == "suspicious":
        head = f"检出 {c['medium'] + c['low']} 项可疑信号"
    elif agg["verdict"] == "inconclusive":
        head = "扫描未完整完成，不下安全结论"
    else:
        head = "在已覆盖范围内未检出 AI 攻击特征"
    return (f"{head}；覆盖 {coverage.get('files_scanned', 0)} 个文件 / "
            f"{coverage.get('bytes_scanned', 0)} 字节"
            + ("（已截断，未扫完）" if coverage.get("truncated") else "") + "。")


def _unique_path(path: Path) -> Path:
    """不覆盖已有文件：同名时追加 -1/-2 序号（P1-9）。"""
    if not path.exists():
        return path
    for i in range(1, 100):
        alt = path.with_name(f"{path.stem}-{i}{path.suffix}")
        if not alt.exists():
            return alt
    return path.with_name(f"{path.stem}-{int(time.time())}{path.suffix}")


def write_reports(findings: list[dict], agg: dict, coverage: dict,
                  out_dir: Path | None) -> dict:
    """findings>10 或用户 --out 时落盘 report.jsonl + summary.md（证据为脱敏形态）。"""
    target = out_dir or Path(tempfile.gettempdir()) / f"{SKILL_NAME}-{int(time.time())}"
    target.mkdir(parents=True, exist_ok=True)
    report_path = _unique_path(target / "report.jsonl")
    summary_path = _unique_path(target / "summary.md")
    reds = [redact_finding(f) for f in findings]
    report_path.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in reds) + "\n",
        encoding="utf-8")
    lines = [f"# AI 内容安检报告（{SKILL_NAME} v{SKILL_VERSION}）", "",
             f"- 判决：**{_risk_word(agg['verdict'])}**（verdict={agg['verdict']}，"
             f"来源=引擎，confidence={agg['confidence']}）",
             f"- 计数：{json.dumps(agg['counts'], ensure_ascii=False)}",
             f"- 覆盖：{coverage.get('files_scanned', 0)} 文件 / "
             f"{coverage.get('bytes_scanned', 0)} 字节"
             + ("（截断）" if coverage.get("truncated") else ""), ""]
    if coverage.get("sensitive_skipped"):
        lines.append(f"- 敏感文件仅报存在（未读取）：{', '.join(coverage['sensitive_skipped'])}")
    lines += ["## 命中明细（证据已脱敏）", ""]
    for r in reds:
        lines += [f"- **[{r['severity']}] {r['title']}** `{r['file']}:{r['line']}`",
                  f"  - {r['evidence_redacted']}",
                  f"  - 建议：{r.get('advice')}", ""]
    lines += ["---", "*零命中仅代表当前规则集未发现命中，不代表内容绝对安全。*",
              f"*依据 Arcanum Prompt Injection Taxonomy v{PITAX_VERSION}（CC BY 4.0）。*"]
    summary_path.write_text("\n".join(lines), encoding="utf-8")
    return {"report_path": str(report_path),
            "summary_path": str(summary_path)}


def build_envelope(findings: list[dict], agg: dict, coverage: dict,
                   report_paths: dict | None, elapsed_ms: int) -> dict:
    top = sorted(findings, key=lambda f: _SEVERITY_RANK.get(
        str(f.get("severity", "info")).lower(), 4))[:10]
    env = {
        "schema_version": SCHEMA_VERSION, "skill": SKILL_NAME,
        "skill_version": SKILL_VERSION, "pitax_version": PITAX_VERSION,
        "ok": True, "verdict": agg["verdict"], "verdict_source": "engine",
        "confidence": agg["confidence"],
        "summary": build_summary_text(agg, coverage),
        "ambient": {"one_liner": (
            f"未检出已知攻击特征（{build_summary_text(agg, coverage)}零命中不代表绝对安全）"
            if agg["verdict"] == "clean" else
            f"⚠️ {build_summary_text(agg, coverage)}——建议先查看报告再决定是否采用该内容")},
        "counts": agg["counts"], "coverage": coverage,
        "top_findings": [redact_finding(f) for f in top],
        "elapsed_ms": elapsed_ms,
        "limits": ["零命中仅代表当前规则集未发现命中，不代表内容绝对安全"],
    }
    if report_paths:
        env.update(report_paths)
    return env


def _sanitize_for_sarif(findings: list[dict]) -> list[dict]:
    """SARIF 源头洗洗：description 内嵌的证据原文、pitax.evidence/decoded_payload
    在进入 build_sarif 之前替换/移除——SARIF 的 message/fullDescription/properties
    均由这些字段派生，源头干净则产物干净（零原文口径）。"""
    out = []
    for f in findings:
        g = dict(f)
        raw_ev = (f.get("code_snippet") or "")[:240]
        g["description"] = _scrub_description(str(f.get("description") or ""), raw_ev)
        pit = f.get("pitax")
        if isinstance(pit, dict):
            p2 = dict(pit)
            ev = p2.get("evidence")
            if ev:
                ev = str(ev)
                p2["evidence"] = "[len={len} sha={sha} frag={frag}]".format(
                    len=len(ev), sha=_sha8(ev), frag=_teaser(ev))
            p2.pop("decoded_payload", None)
            g["pitax"] = p2
        out.append(g)
    return out


def _redact_sarif(doc: dict) -> dict:
    """SARIF 输出脱敏（零原文口径，wrapper 层后处理，不改锚内 sarif.py）：
    fullDescription/message/properties.evidence 中的证据原文一律替换；
    informationUri 指向本仓；decoded_payload 只留长度+哈希。"""
    doc.setdefault("runs", [])
    for run in doc["runs"]:
        driver = run.get("tool", {}).get("driver", {})
        _repo_uri = "https://github.com/a9320/tianxi-ai-content-guard"
        if driver.get("informationUri") and driver.get("informationUri") != _repo_uri:
            driver["informationUri"] = _repo_uri
        for rd in driver.get("rules", []):
            fd = rd.get("fullDescription", {}).get("text", "")
            if len(fd) > 400:  # 超长描述截断（正常规则卡不会这么长）
                rd["fullDescription"]["text"] = fd[:400] + "…"
        for r in run.get("results", []):
            props = (r.get("properties") or {}).get("pitax") or {}
            ev = str(props.get("evidence") or "")
            scrub = "[证据已脱敏]" if ev else None
            for holder in (r.get("message", {}),
                           (r.get("properties") or {}).get("rule", {}) or {}):
                txt = str(holder.get("text", ""))
                if ev and (ev in txt or ev[:30] in txt):
                    txt = txt.replace(ev, scrub).replace(ev[:30], scrub)
                if " | decoded payload:" in txt:
                    txt = txt.split(" | decoded payload:")[0] + " | decoded payload: [已脱敏]"
                holder["text"] = txt
            if ev and not str(ev).startswith("[len="):
                props["evidence"] = "[len={len} sha={sha} frag={frag}]".format(
                    len=len(ev), sha=_sha8(ev), frag=_teaser(ev))
            if props.get("decoded_payload"):
                dec = _mask_secrets(str(props["decoded_payload"]))
                props["decoded_payload"] = f"[redacted] len={len(dec)} sha={_sha8(dec)}"
    return doc


# ══════════════════════ stdin 宽容解析 ══════════════════════

def _unwrap_stdin_json(obj) -> str | None:
    """五形态宽容解析：{"params":{"input":..}} / {"input":..} / text/content/prompt / 裸文本。"""
    if isinstance(obj, dict):
        if isinstance(obj.get("params"), dict):
            obj = obj["params"]
        for key in ("input", "text", "content", "prompt"):
            v = obj.get(key)
            if isinstance(v, str) and v.strip():
                return v
    return None


def read_stdin_text() -> str:
    """编码三件套（第 2 件）：stdin 读原始字节，链解 + JSON 宽容解包，兜底裸文本。"""
    raw = sys.stdin.buffer.read()
    if not raw:
        return ""
    text = None
    try:
        text = _unwrap_stdin_json(json.loads(raw.decode("utf-8-sig")))
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        text = None
    return text if text is not None else _decode_bytes(raw)


# ══════════════════════ 自检与解码复核 ══════════════════════

def self_check() -> int:
    engine_dir = _SCRIPT_DIR / "engine"
    print(f"{SKILL_NAME} v{SKILL_VERSION} self-check")
    print(f"python: {sys.version.split()[0]}   pitax: v{PITAX_VERSION}   rules: {len(ALL_RULES)}")
    print("network: none（无 requests/urllib/socket/http.client 导入，零联网）")
    print("dynamic execution: none（无 eval/exec/os.system/subprocess/pickle.loads；compile 仅 re.compile 正则）")
    print("writes: none by default（仅 findings>10 或 --out 时写脱敏报告；同名不覆盖，自动加序号）")
    print("reads: 只读用户指定路径（--file 与 --dir 同口径防护）；系统目录拒绝；"
          "敏感文件(.env/*.pem/id_rsa 等)拒绝读取只报存在；符号链接/junction 不跟随")
    anchor = engine_dir / "ENGINE-ANCHOR.txt"
    for p in sorted(engine_dir.glob("*.py")):
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        print(f"engine file: {p.name}  sha256={h[:16]}…")
    if anchor.exists():
        skill_root = _SCRIPT_DIR.parent
        for ln in anchor.read_text(encoding="utf-8").splitlines():
            if "  " not in ln:
                continue
            want, rel = ln.split("  ", 1)
            rel = rel.strip()
            target = skill_root / pathlib_posix(rel.replace("skill/", "", 1))                 if rel.startswith("skill/") else engine_dir / rel
            got = hashlib.sha256(target.read_bytes()).hexdigest()
            print(f"anchor: {rel}  {'MATCH' if got == want.strip() else 'MISMATCH!!'}")
    return 0


def decode_review(payload: str, show_fragment: bool = False) -> int:
    """编码载荷分层复核（≤3 层 / ≤64KB，只解码匹配，不执行）。
    默认不打印明文片段（防泄露）；--show-fragment 显式查看（片段仍过脱敏）。"""
    data = payload[:64 * 1024]
    print(f"输入 len={len(payload)} sha={_sha8(payload)}")
    for layer in range(1, 4):
        cand = data.strip()
        if not _B64_CANDIDATE_RE.match(cand):
            print(f"layer {layer}: 非 base64 候选，停止剥离")
            break
        try:
            peeled = base64.b64decode(cand, validate=True).decode("utf-8", errors="replace")
        except (binascii.Error, ValueError):
            print(f"layer {layer}: base64 解码失败，停止剥离")
            break
        line = f"layer {layer}: len={len(peeled)} sha={_sha8(peeled)}"
        if show_fragment:
            line += f" frag={redact_fragment(peeled)}"
        print(line)
        if len(peeled) >= 256 * 1024:
            print("达到 256KB 解码输出上限，停止")
            break
        data = peeled
    return 0


# ══════════════════════ main ══════════════════════

def _err(code: str, field: str, message: str, hint: str = "") -> int:
    json.dump({"ok": False, "error_code": code, "field": field,
               "message": message, "hint": hint},
              sys.stdout, ensure_ascii=False)
    sys.stdout.write("\n")
    # 契约：2=参数/输入类错误（含防护拒绝），3=运行时错误
    return 2 if code in ("INVALID_ARGUMENT", "NOT_FOUND", "GUARD_REJECTED") else 3


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="entry.py",
        description="AI 内容安检：PITAX 确定性检测提示注入/隐形字符/编码载荷/AI 配置后门。")
    ap.add_argument("--text", help="直接传入待检文本（短文本 <8KB）")
    ap.add_argument("--file", help="待检文件路径（- 表示读 stdin）")
    ap.add_argument("--dir", dest="dir_path", help="待检目录/仓库（递归只读扫描）")
    ap.add_argument("--mode", choices=["auto", "config"], default="auto",
                    help="config=仅审计 AI 配置文件（.cursor/rules、CLAUDE.md 等）")
    ap.add_argument("--format", choices=["json", "markdown"], default="json")
    ap.add_argument("--min-severity", choices=["critical", "high", "medium"])
    ap.add_argument("--fail-on", choices=["critical", "high", "medium"],
                    help="发现该级别及以上命中时退出码 1（CI 用）")
    ap.add_argument("--max-files", type=int, default=DEFAULT_MAX_FILES)
    ap.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    ap.add_argument("--max-depth", type=int, default=DEFAULT_MAX_DEPTH)
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_S)
    ap.add_argument("--out", help="报告输出目录（默认：仅 findings>10 时写系统临时目录）")
    ap.add_argument("--sarif", help="导出 SARIF 2.1.0 到指定文件（仓库模式用）")
    ap.add_argument("--decode", help=argparse.SUPPRESS)
    ap.add_argument("--show-fragment", action="store_true",
                    help="--decode 时显式查看脱敏片段（默认只给长度+哈希）")
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--version", action="version",
                    version=f"{SKILL_NAME} {SKILL_VERSION}")
    args = ap.parse_args(argv)

    if args.self_check:
        return self_check()
    if args.decode is not None:
        return decode_review(args.decode, show_fragment=args.show_fragment)

    # session JSONL 遥测锚：每次执行在 stderr 留稳定标记，供触发率统计
    print(f"[{SKILL_NAME}] v{SKILL_VERSION} engine=pitax-{PITAX_VERSION}",
          file=sys.stderr)

    inputs = [x for x in (args.text, args.file, args.dir_path) if x]
    if len(inputs) != 1:
        return _err("INVALID_ARGUMENT", "text|file|dir",
                    "必须且只能提供 --text / --file / --dir 之一",
                    "长文本请写入临时文件后用 --file，勿走命令行参数")
    if args.text is not None and not args.text.strip():
        return _err("INVALID_ARGUMENT", "text", "待检文本为空",
                    "提供非空内容，或用 --file 指定文件")

    # v1.3.3 扫描限制参数范围校验（外部评审 B：负数/异常值导致扫描行为偏离预期）
    for flag, val, lo, hi in (("max-files", args.max_files, 1, 100000),
                              ("max-bytes", args.max_bytes, 1, 1 << 30),
                              ("max-depth", args.max_depth, 1, 512),
                              ("timeout", args.timeout, 1, 3600)):
        if not lo <= val <= hi:
            return _err("INVALID_ARGUMENT", flag, f"{flag}={val} 超出允许范围",
                        f"取值须为 {lo}..{hi} 的整数")

    started = time.monotonic()
    findings: list[dict] = []
    coverage: dict = {}
    errors: list[str] = []
    try:
        if args.text is not None:
            findings, coverage, errors = collect_text(args.text)
        elif args.file is not None:
            if args.file == "-":
                stdin_text = read_stdin_text()
                if not stdin_text.strip():
                    return _err("INVALID_ARGUMENT", "file", "stdin 输入为空",
                                "提供非空内容")
                findings, coverage, errors = collect_text(stdin_text)
            else:
                fpath = Path(args.file).expanduser()
                if not fpath.is_file():
                    return _err("NOT_FOUND", "file", f"文件不存在：{fpath}")
                # 先防护后 resolve（#37）：guard 内部先查 symlink 再 resolve，
                # 与 dir mode 的 no-follow 承诺同口径
                _guard_file(fpath)  # P0-3：file mode 与 dir mode 同防护口径
                fpath = fpath.resolve()
                # 传保留路径结构的字符串（非 basename），让 .cursor/rules 等
                # AI 配置路径在单文件模式下仍可识别（P0-2）
                path_hint = args.file.replace("\\", "/")
                findings = scan_file(path_hint, _decode_bytes(_read_file_bytes(fpath)))
                findings = _post_filter(findings)
                coverage = {"root": str(fpath), "files_scanned": 1, "files_skipped": 0,
                            "dirs_skipped": 0, "dirs_skipped_names": [],
                            "sensitive_skipped": [], "bytes_scanned": fpath.stat().st_size,
                            "truncated": False, "limits": [
                                "确定性层仅覆盖 PITAX 规则集；语义改写类攻击不在本层覆盖内"]}
        else:
            root = guard_root(args.dir_path)
            if not root.exists():
                return _err("NOT_FOUND", "dir", f"目录不存在：{root}")
            files_map, coverage, errors = collect_dir(
                root, args.max_files, args.max_bytes, args.max_depth,
                args.timeout, config_only=(args.mode == "config"))
            findings = _post_filter(scan_repo(files_map))
    except ValueError as exc:
        return _err("GUARD_REJECTED", "path", str(exc),
                    "系统目录/敏感路径/超大文件被防护策略拒绝")
    except (PermissionError, OSError) as exc:
        return _err("RUNTIME_ERROR", "path", f"{type(exc).__name__}: {exc}")

    findings = _dedup(findings)
    agg = aggregate(findings, coverage, errors)  # 判决一律基于全量命中（修 R2-5）
    display = findings
    if args.min_severity:
        floor = _SEVERITY_RANK[args.min_severity]
        display = [f for f in findings if _SEVERITY_RANK.get(
            str(f.get("severity", "info")).lower(), 4) <= floor]
    report_paths = None
    try:
        if findings and (len(findings) > 10 or args.out):
            report_paths = write_reports(findings, agg, coverage,
                                         Path(args.out) if args.out else None)
    except OSError as exc:
        return _err("INVALID_ARGUMENT", "out", f"报告路径不可写：{exc}")
    envelope = build_envelope(display, agg, coverage, report_paths,
                              int((time.monotonic() - started) * 1000))
    if args.min_severity and len(display) < len(findings):
        envelope["display_filtered_out"] = len(findings) - len(display)
    if args.sarif:
        try:
            sarif_path = _unique_path(Path(args.sarif))
            sarif_path.parent.mkdir(parents=True, exist_ok=True)
            sarif_path.write_text(
                json.dumps(_redact_sarif(build_sarif(_sanitize_for_sarif(findings),
                                                      SKILL_NAME, SKILL_VERSION)),
                           ensure_ascii=False, indent=2), encoding="utf-8")
        except OSError as exc:
            return _err("INVALID_ARGUMENT", "sarif", f"SARIF 路径不可写：{exc}")
        envelope["sarif_path"] = str(sarif_path)

    if args.format == "markdown":
        print(f"## {_risk_word(agg['verdict'])}（{agg['verdict']}）")
        print(envelope["summary"])
        print()
        for r in envelope["top_findings"]:
            print(f"- [{r['severity']}] {r['title']} `{r['file']}:{r['line']}`")
            print(f"  - {r['evidence_redacted']}")
        print()
        print("零命中仅代表当前规则集未发现命中，不代表内容绝对安全。")
    else:
        json.dump(envelope, sys.stdout, ensure_ascii=False, indent=2)
        sys.stdout.write("\n")

    if args.fail_on and any(_SEVERITY_RANK.get(
            str(f.get("severity", "info")).lower(), 4) <= _SEVERITY_RANK[args.fail_on]
            for f in findings):  # 全量判定，--min-severity 不可绕过（修 R2-5）
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
