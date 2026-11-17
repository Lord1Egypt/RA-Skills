"""PITAX 确定性检测器 — 与官方 taxonomy v1.6.1 编号对齐。

规则 → 检测函数：
  PIT-E-23  detect_invisible_text      不可见字符走私（零宽/软连字符/U+E0000 标签）
  PIT-E-54  detect_trojan_source       Bidi 双向控制符源码欺骗（CVE-2021-42574）
  PIT-T-46  detect_ai_config_injection AI 指令文件后门（.cursor/rules 等）
  PIT-T-51  detect_comment_injection   代码注释指令覆盖
  PIT-N-06  detect_doc_injection       项目文档投毒（README 等）
  PIT-E-07/14/36/57  detect_encoded_payloads  单层/多层编码载荷

设计原则（整合版方案铁律）：
- 只做确定性高的检测，控制误报；
- 编码检测仅在解码后命中注入关键词才报告（避免对普通 base64 误报）；
- 每条 finding 携带 PITAX 编号 + ATLAS/CVE 映射 + 参考链接，可复现、可引用。

Based on the Arcanum Prompt Injection Taxonomy by Jason Haddix,
Arcanum Information Security (arcanum-sec.com). CC BY 4.0.
"""
from __future__ import annotations

import base64
import codecs
import re
import os
from dataclasses import dataclass, field

from .rules import get_rule
from .descriptions_en import description_for, suggestion_for

# ────────────────────────── 数据结构 ──────────────────────────
@dataclass
class Finding:
    pitax_code: str
    file: str
    line: int
    evidence: str
    message: str
    severity: str | None = None
    decoded_payload: str | None = None
    extra: dict = field(default_factory=dict)

    def to_report_dict(self, finding_id: str, language: str = "text") -> dict:
        rule = get_rule(self.pitax_code)
        sev = self.severity or rule.get("severity", "medium")
        # 单层编码子类确定性稍低，置信度 70；其余 90
        confidence = 70 if self.pitax_code in ("PIT-E-07", "PIT-E-14", "PIT-E-36") else 90
        return {
            "id": finding_id,
            "type": self.pitax_code,
            "title": f"[{self.pitax_code}] {rule['name']}",
            "severity": sev,
            "confidence": confidence,
            "cwe": rule.get("cwe"),
            "mitre_atlas": rule.get("mitre_atlas"),
            "description": description_for(self.pitax_code, self.message),
            "file": self.file,
            "line": self.line,
            "language": language,
            "code_snippet": self.evidence[:240],
            "agent": "agent_0_sanitizer",
            "suggestion": suggestion_for(
                "移除隐藏内容/恶意指令；若为误报请在 CI 中标记豁免并说明理由。"
            ),
            "pitax": {
                "code": self.pitax_code,
                "name": rule["name"],
                "pillar": rule["pillar"],
                "aliases": rule.get("aliases", []),
                "references": rule.get("references", []),
                "cwe": rule.get("cwe"),
                "mitre_atlas": rule.get("mitre_atlas"),
                "cve": rule.get("cve"),
                "evidence": self.evidence[:120],
                "decoded_payload": self.decoded_payload,
                **self.extra,
            },
        }


# ────────────────── PIT-E-23: 不可见字符走私 ──────────────────
# 人类不可见、但会被 LLM 解析的格式字符。不含 Bidi 覆盖类（归 PIT-E-54）。
INVISIBLE_CHARS: dict[str, str] = {
    "\u200b": "Zero-Width Space",
    "\u200c": "Zero-Width Non-Joiner",
    "\u200d": "Zero-Width Joiner",
    "\u200e": "Left-to-Right Mark",
    "\u200f": "Right-to-Left Mark",
    "\u2060": "Word Joiner",
    "\u2061": "Function Application",
    "\u2062": "Invisible Times",
    "\u2063": "Invisible Separator",
    "\u2064": "Invisible Plus",
    "\ufeff": "Zero-Width No-Break Space (BOM)",
    "\u00ad": "Soft Hyphen",
    "\u034f": "Combining Grapheme Joiner",
    "\u061c": "Arabic Letter Mark",
    "\u115f": "Hangul Choseong Filler",
    "\u1160": "Hangul Jungseong Filler",
    "\u17b4": "Khmer Vowel Inherent Aq",
    "\u17b5": "Khmer Vowel Inherent Aa",
    "\u180e": "Mongolian Vowel Separator",
}
# U+E0000–U+E007F 标签字符区段（ASCII Smuggling 关键载体）
TAG_RANGE = (0xE0000, 0xE007F)
_WHITESPACE = set(" \t\r\n")


def detect_invisible_text(code: str, file: str) -> list[Finding]:
    findings: list[Finding] = []
    hits: dict[str, list[int]] = {}
    for lineno, line in enumerate(code.splitlines(), start=1):
        for ch in line:
            if ch in _WHITESPACE:
                continue
            label = INVISIBLE_CHARS.get(ch)
            if label is None and TAG_RANGE[0] <= ord(ch) <= TAG_RANGE[1]:
                label = "TAG CHARACTER (ASCII Smuggling)"
            if label:
                hits.setdefault(f"U+{ord(ch):04X} {label}", []).append(lineno)
    for label, lines in hits.items():
        findings.append(Finding(
            pitax_code="PIT-E-23",
            file=file,
            line=lines[0],
            evidence=f"{label} at line(s) {lines[:5]}",
            message=(
                f"检测到不可见 Unicode 字符（{label}，共 {len(lines)} 行出现）。"
                "不可见字符常用于在人类阅读不可见的情况下向 LLM 走私指令。"
            ),
            extra={"occurrence_lines": lines[:20]},
        ))
    return findings


# ────────────────── PIT-E-54: Trojan Source（Bidi 欺骗）──────────────────
# 双向文本控制符：改变源码视觉呈现顺序（CVE-2021-42574，trojansource.codes）。
BIDI_CHARS: dict[str, str] = {
    "\u202a": "Left-to-Right Embedding",
    "\u202b": "Right-to-Left Embedding",
    "\u202c": "Pop Directional Formatting",
    "\u202d": "Left-to-Right Override",
    "\u202e": "Right-to-Left Override",
    "\u2066": "Left-to-Right Isolate",
    "\u2067": "Right-to-Left Isolate",
    "\u2068": "First Strong Isolate",
    "\u2069": "Pop Directional Isolate",
}


def detect_trojan_source(code: str, file: str) -> list[Finding]:
    """整个文件聚合为一条 finding（同一文件的 Bidi 作弊字符属于同一攻击）。"""
    hits: list[tuple[int, str]] = []  # (lineno, label)
    for lineno, line in enumerate(code.splitlines(), start=1):
        for ch in line:
            label = BIDI_CHARS.get(ch)
            if label:
                hits.append((lineno, f"U+{ord(ch):04X} {label}"))
    if not hits:
        return []
    lines = sorted({ln for ln, _ in hits})
    labels = [lb for _, lb in hits]
    return [Finding(
        pitax_code="PIT-E-54",
        file=file,
        line=lines[0],
        evidence="; ".join(labels[:5]) + ("..." if len(labels) > 5 else ""),
        message=(
            f"检测到双向文本控制符（{', '.join(sorted(set(labels))[:3])}，"
            f"共 {len(hits)} 处）。Bidi 字符可改变源码视觉呈现顺序（Trojan Source，"
            "CVE-2021-42574），使代码看起来与实际逻辑不一致，同时欺骗人类评审与 AI 助手。"
        ),
        extra={"occurrence_lines": lines[:20]},
    )]


# ────────────────── PIT-T-46: AI 指令文件后门 ──────────────────
AI_CONFIG_BASENAMES = {
    ".cursor/rules", "cursor.rules", "claude.md", "claudemd.md",
    "copilot-instructions.md", "agents.md", ".cursorrules", ".windsurfrules",
    ".clinerules", ".windsurf/rules",
}


def is_ai_config_path(path: str) -> bool:
    p = path.lower().replace("\\", "/")
    for cfg in AI_CONFIG_BASENAMES:
        if p == cfg.lower() or p.endswith("/" + cfg.lower()):
            return True
    # 目录包含 .cursor / .windsurf 且文件名含 rules/instructions
    parts = p.strip("/").split("/")
    if any(part in (".cursor", ".windsurf") for part in parts[:-1]):
        if parts[-1].endswith("rules") or "instruction" in parts[-1]:
            return True
        # 路径父目录是 .cursor/rules 或 .windsurf/rules → 其下文件都是 AI 配置文件
        if "rules" in parts[:-1]:
            return True
    return False


_CONFIG_PATTERNS = [
    r"(?i)ignore\s+(all\s+)?previous\s+instructions",
    # 2026-11-01 Copilot 现场漏报 PS03 实证："SYSTEM OVERRIDE: ignore safety rules…" 0 命中
    r"(?i)ignore\s+(all\s+)?(?:previous\s+)?(?:safety|security)\s+(?:rules|guidelines)",
    r"(?i)system\s+overrides?\b",
    r"(?i)override\s+(all\s+)?(previous\s+)?instructions",
    r"(?i)disregard\s+(all\s+)?(previous\s+)?instructions",
    r"(?i)system\s*prompt",
    r"(?i)you\s+are\s+now",
    r"(?i)\bDAN\s+mode\b",
    r"(?i)developer\s+mode\b",
    r"(?i)(?:enable|enter|activate)\s+(?:the\s+)?jailbreak|jailbreak\s+mode",
    r"(?i)disable\s+safety\s+guidelines",
    r"(?i)bypass\s+(all\s+)?safety",
    r"忽略(?:之前|以前|上面|上述)(?:的)?(?:所有)?(?:指令|提示|要求)",
    r"无视(?:之前|以前|上面|上述)(?:的)?(?:所有)?(?:指令|提示|要求)",
    r"你现在(?:是|成为)(?:一名)?(?:攻击者|黑客)",
    r"绕过(?:所有)?安全",
    r"以前の指示を無視",
    r"跳过(?:所有)?安全",
]
_CONFIG_RE = [re.compile(p) for p in _CONFIG_PATTERNS]

# 防御性写法（"Never reveal the system prompt"）是合规建议，不是注入（NEG-3 实证）
_SYSTEM_PROMPT_PATTERN = r"(?i)system\s*prompt"
_DEFENSIVE_RE = re.compile(
    r"(?i)\b(?:never|don'?t|do not|must not|should not|refuse|avoid)\b|严禁|禁止|不要|不得"
)


def _is_defensive(rx: re.Pattern[str], line: str) -> bool:
    return rx.pattern == _SYSTEM_PROMPT_PATTERN and bool(_DEFENSIVE_RE.search(line))


def detect_ai_config_injection(code: str, file: str) -> list[Finding]:
    """只对 AI 指令文件路径检测（.cursor/rules、CLAUDE.md 等）。"""
    findings: list[Finding] = []
    hits: dict[re.Pattern, list[int]] = {}
    cfg_lines = code.splitlines()
    for lineno, line in enumerate(cfg_lines, start=1):
        window = line if lineno >= len(cfg_lines) else f"{line} {cfg_lines[lineno]}"
        for rx in _CONFIG_RE:
            if rx.search(window) and not _is_defensive(rx, line):
                hits.setdefault(rx, []).append(lineno)
    for rx, lines in hits.items():
        match = rx.search(code.splitlines()[lines[0] - 1])
        evidence = match.group(0) if match else "config injection pattern"
        findings.append(Finding(
            pitax_code="PIT-T-46",
            file=file,
            line=lines[0],
            evidence=evidence[:120],
            message=(
                f"AI 指令文件中检测到指令覆盖/角色劫持模式（{evidence[:60]}，"
                f"共 {len(lines)} 行出现）。攻击者可能在仓库的 AI 助手配置中植入后门"
                "（同 CVE-2025-53773 攻击模式）。"
            ),
            extra={"occurrence_lines": lines[:20]},
        ))
    return findings


# ────────────────── PIT-N-06: 项目文档投毒 ──────────────────
DOC_EXTENSIONS = {".md", ".mdc", ".markdown", ".rst", ".txt"}


def is_doc_path(path: str) -> bool:
    p = path.lower().replace("\\", "/")
    if is_ai_config_path(p):  # AI 指令文件归 PIT-T-46 管
        return False
    import os
    return os.path.splitext(p)[1] in DOC_EXTENSIONS


# 与注释注入同一组高置信度模式，另加 disable/bypass safety（文档语境常见）
_DOC_INJECT_RE = [re.compile(p) for p in _CONFIG_PATTERNS]


def _quote_context(line: str, in_fence: bool) -> str:
    """引用语境标注：围栏代码块 / 引用块 / 行内代码。检出不变，只给研判提示。"""
    if in_fence:
        return "fenced"
    stripped = line.lstrip()
    if stripped.startswith(">"):
        return "blockquote"
    if line.count("`") >= 2:
        return "inline-code"
    return ""


def detect_doc_injection(code: str, file: str) -> list[Finding]:
    findings: list[Finding] = []
    hits: dict[re.Pattern, list[int]] = {}
    contexts: dict[int, str] = {}
    doc_lines = code.splitlines()
    in_fence = False
    for lineno, line in enumerate(doc_lines, start=1):
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_fence = not in_fence
            continue
        context = _quote_context(line, in_fence)
        window = line if lineno >= len(doc_lines) else f"{line} {doc_lines[lineno]}"
        for rx in _DOC_INJECT_RE:
            if rx.search(window) and not _is_defensive(rx, line):
                hits.setdefault(rx, []).append(lineno)
                contexts[lineno] = context
    for rx, lines in hits.items():
        match = rx.search(code.splitlines()[lines[0] - 1])
        evidence = match.group(0) if match else "doc injection pattern"
        findings.append(Finding(
            pitax_code="PIT-N-06",
            file=file,
            line=lines[0],
            evidence=evidence[:120],
            message=(
                f"项目文档中检测到面向 AI Agent 的指令注入模式（{evidence[:60]}，"
                f"共 {len(lines)} 行出现）。文档是 Agent 的常规输入，投毒不会被"
                "人类评审与传统工具注意。"
            ),
            extra={
                "occurrence_lines": lines[:20],
                "context": contexts.get(lines[0], ""),
            },
        ))
    return findings


# ────────────────── PIT-T-51: 注释指令覆盖 ──────────────────
_COMMENT_INJECT_PATTERNS = [
    r"(?i)\bignore\s+(all\s+)?previous\s+instructions\b",
    # 2026-11-01 Copilot 现场漏报 PS03 同源：注释族同样补 safety/security rules 与 system override
    r"(?i)\bignore\s+(all\s+)?(?:previous\s+)?(?:safety|security)\s+(?:rules|guidelines)\b",
    r"(?i)\bsystem\s+overrides?\b",
    r"(?i)\breveal\s+the\s+system\s+prompt\b",
    r"(?i)\breveal\s+your\s+(system\s+)?prompt\b",
    r"(?i)\bdisregard\s+(all\s+)?(previous\s+)?instructions\b",
    r"(?i)\byou\s+are\s+now\s+(an?\s+)?(attacker|hacker|assistant)\b",
    r"(?i)\byou\s+are\s+an?\s+(attacker|hacker|assistant)\b",
    r"(?i)\bdeveloper\s+mode\b",
    r"(?i)\bDAN\s+mode\b",
    r"忽略(?:之前|以前|上面|上述)(?:的)?(?:所有)?(?:指令|提示|要求)",
    r"无视(?:之前|以前|上面|上述)(?:的)?(?:所有)?(?:指令|提示|要求)",
    r"你现在(?:是|成为)(?:一名)?(?:攻击者|黑客)",
    r"绕过(?:所有)?安全",
    r"以前の指示を無視",
    r"跳过(?:所有)?安全",
]
_COMMENT_INJECT_RE = [re.compile(p) for p in _COMMENT_INJECT_PATTERNS]

# 注释标记按扩展名取：字符串里的 % / ; / -- 不是注释起点
# （2026-10-30 PITAX 基准 NEG-4 实证：`"100% ignore previous instructions"` 曾误报 PIT-T-51）
_COMMENT_MARKERS: dict[str, tuple[str, ...]] = {
    ".py": ("#",), ".sh": ("#",), ".bash": ("#",), ".rb": ("#",), ".r": ("#",),
    ".yaml": ("#",), ".yml": ("#",), ".toml": ("#",), ".cfg": ("#",),
    ".ini": ("#", ";"),
    ".js": ("//", "/*"), ".ts": ("//", "/*"), ".jsx": ("//", "/*"), ".tsx": ("//", "/*"),
    ".java": ("//", "/*"), ".go": ("//", "/*"), ".rs": ("//", "/*"),
    ".c": ("//", "/*"), ".cpp": ("//", "/*"), ".h": ("//", "/*"),
    ".php": ("//", "/*", "#"), ".vue": ("//", "/*", "<!--"),
    ".sql": ("--", "/*"), ".lua": ("--",),
    ".html": ("<!--",), ".htm": ("<!--",),
}
_DEFAULT_COMMENT_MARKERS = ("#", "//", "/*", "<!--", "*")


def _extract_comment(line: str, path: str = "") -> str | None:
    """按扩展名取注释标记，返回最早出现的注释片段。"""
    ext = os.path.splitext(path.lower())[1]
    markers = _COMMENT_MARKERS.get(ext, _DEFAULT_COMMENT_MARKERS)
    best = -1
    for marker in markers:
        idx = line.find(marker)
        if idx >= 0 and (best < 0 or idx < best):
            best = idx
    return line[best:] if best >= 0 else None


def detect_comment_injection(code: str, file: str) -> list[Finding]:
    findings: list[Finding] = []
    hits: dict[re.Pattern, list[int]] = {}
    cm_lines = code.splitlines()
    for lineno, line in enumerate(cm_lines, start=1):
        comment = _extract_comment(line, file)
        if comment is None:
            continue
        nxt = _extract_comment(cm_lines[lineno], file) if lineno < len(cm_lines) else None
        # 去掉注释标记再拼接：跨行拆分常写成 "# ignore previous" / "# instructions"
        body = comment.lstrip("#/*<!-> 	")
        window = body if not nxt else f"{body} {nxt.lstrip('#/*<!-> 	')}"
        for rx in _COMMENT_INJECT_RE:
            if rx.search(window):
                hits.setdefault(rx, []).append(lineno)
    for rx, lines in hits.items():
        match = rx.search(code.splitlines()[lines[0] - 1])
        evidence = match.group(0) if match else "comment injection pattern"
        findings.append(Finding(
            pitax_code="PIT-T-51",
            file=file,
            line=lines[0],
            evidence=evidence[:120],
            message=(
                f"代码注释中检测到提示注入指令模式（{evidence[:60]}）。"
                "当 LLM 阅读该代码/注释时可能被劫持，执行非预期指令。"
            ),
            extra={"occurrence_lines": lines[:20]},
        ))
    return findings


# ────────────────── PIT-E-07/14/36/57: 编码载荷 ──────────────────
_ENCODED_TARGET_PATTERNS = [
    r"(?i)\bignore\s+(all\s+)?previous\s+instructions\b",
    r"(?i)\breveal\s+(the\s+)?(system|your)\s+prompt\b",
    r"(?i)\bemail\s+(the\s+)?api\s+keys?\b",
    r"(?i)\bexfiltrate\b",
    r"(?i)\bdeveloper\s+mode\b",
    r"(?i)\byou\s+are\s+now\b",
    r"(?i)\bjailbreak\b",
    r"你现在(?:是|成为)(?:一名)?(?:攻击者|黑客)",
    r"绕过(?:所有)?安全",
    r"以前の指示を無視",
    r"忽略(?:之前|以前|上述)(?:的)?(?:所有)?指令",
]
_ENCODED_TARGET_RE = [re.compile(p) for p in _ENCODED_TARGET_PATTERNS]

# 字符串字面量候选：引号包裹的 8+ 字符串（不含引号/换行；原 20——2026-10-31 基准 E36-2 实证9 字中文反转载荷漏检，误报由解码+关键词门控制）。
# 不再限制字符集——编码判定交给分层解码器（b64 严格校验/rot13/reverse 命中关键词才剥层），
# 否则带空格的 ROT13/反转载荷会漏检。
_STR_LITERAL = re.compile(r'(["\'`])([^"\'`\n]{8,})\1')
# 2026-11-01 Copilot 现场漏报#3（CA03 实证）：载荷躲进注释——注释内容同样过剥层解码
_COMMENT_TOKEN = re.compile(r"[A-Za-z0-9+/=]{16,}")
_B64_STRICT = re.compile(r"[A-Za-z0-9+/]+={0,2}")
_MIN_DECODE_LEN = 16
_MAX_LAYERS = 5

_LAYER_TO_CODE = {
    ("base64",): "PIT-E-07",
    ("rot13",): "PIT-E-14",
    ("reverse",): "PIT-E-36",
}


def _contains_injection(s: str) -> bool:
    return any(rx.search(s) for rx in _ENCODED_TARGET_RE)


def _try_base64(s: str) -> str | None:
    """严格 base64 解码：字符集/长度合法、严格 UTF-8、≥90% 可打印。
    二进制 blob（图片/哈希/JWT 除外）在此被过滤，控制误报。"""
    t = s.strip()
    if len(t.rstrip("=")) < _MIN_DECODE_LEN:
        return None
    if len(t.rstrip("=")) % 4 == 1 or not _B64_STRICT.fullmatch(t):
        return None
    try:
        decoded = base64.b64decode(t, validate=True).decode("utf-8")
    except Exception:
        return None
    if not decoded:
        return None
    printable = sum(ch.isprintable() or ch in "\r\n\t" for ch in decoded)
    if printable / len(decoded) < 0.9:
        return None
    return decoded


def _peel_layers(raw: str) -> tuple[str, list[str]]:
    """逐层剥离 base64/rot13/reverse，返回 (最终文本, 层序列表)。
    rot13/reverse 只有在解码结果命中注入关键词时才继续剥（控制误报）。"""
    current, layers = raw, []
    for _ in range(_MAX_LAYERS):
        decoded = _try_base64(current)
        if decoded is not None and decoded != current:
            current = decoded
            layers.append("base64")
            continue
        if any(c.isalpha() for c in current):
            rot = codecs.decode(current, "rot_13")
            if rot != current and _contains_injection(rot):
                current = rot
                layers.append("rot13")
                continue
        rev = current[::-1]
        if rev != current and _contains_injection(rev):
            current = rev
            layers.append("reverse")
            continue
        break
    return current, layers


def detect_encoded_payloads(code: str, file: str) -> list[Finding]:
    findings: list[Finding] = []
    for lineno, line in enumerate(code.splitlines(), start=1):
        for m in _STR_LITERAL.finditer(line):
            raw = m.group(2)
            final, layers = _peel_layers(raw)
            if not layers or not _contains_injection(final):
                continue  # 纯明文/未命中关键词 → 不报（控制误报）
            findings.append(_encoded_finding(file, lineno, raw, final, layers))
        # 注释内容同口径：取出注释体里的 base64 形 token 过剥层（解码+关键词双闸控制误报）
        comment = _extract_comment(line, file)
        if comment is None:
            continue
        body = comment.lstrip("#/*<!-> \t")
        seen: set[str] = set()
        for m in _COMMENT_TOKEN.finditer(body):
            raw = m.group(0)
            if raw in seen:
                continue
            seen.add(raw)
            final, layers = _peel_layers(raw)
            if not layers or not _contains_injection(final):
                continue
            findings.append(_encoded_finding(file, lineno, raw, final, layers))
    return findings


def _encoded_finding(file: str, lineno: int, raw: str, final: str, layers: list[str]) -> Finding:
    if len(layers) >= 2:
        pitax_code = "PIT-E-57"
    else:
        pitax_code = _LAYER_TO_CODE.get(tuple(layers), "PIT-E-57")
    return Finding(
        pitax_code=pitax_code,
        file=file,
        line=lineno,
        evidence=raw[:80] + ("..." if len(raw) > 80 else ""),
        message=(
            f"检测到{len(layers)}层编码（{'→'.join(layers)}）的提示注入载荷，"
            "用于规避基于关键词的过滤。"
        ),
        decoded_payload=final[:160],
        extra={"layers": layers},
    )
