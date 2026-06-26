"""Rule-based content type detector for the Fusion Pipeline Cortex.

Detection priority (highest confidence first):
  1. Markdown code fences  → code + language  (0.95)
  2. Diff headers          → diff             (0.95)
  3. JSON parse            → json             (0.90)
  4. Shebang line          → code + language  (0.90)
  5. Log line density      → log              (0.80)
  6. Search result density → search           (0.80)
  7. Code keyword density  → code             (0.70)
  8. Fallback              → text             (0.50)

Part of claw-compactor. License: MIT.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DetectionResult:
    content_type: str   # text | code | json | log | diff | search
    language: str | None
    confidence: float   # 0.0 – 1.0


@dataclass(frozen=True)
class Section:
    content: str
    content_type: str
    language: str | None
    start_line: int
    end_line: int


# ---------------------------------------------------------------------------
# Regex constants
# ---------------------------------------------------------------------------

# Code fence: ```lang  or  ~~~lang  (lang optional)
_FENCE_OPEN = re.compile(r"^(`{3,}|~{3,})([\w+-]*)$", re.MULTILINE)
_FENCE_CLOSE_BACKTICK = re.compile(r"^`{3,}\s*$", re.MULTILINE)
_FENCE_CLOSE_TILDE = re.compile(r"^~{3,}\s*$", re.MULTILINE)

# Diff
_DIFF_HEADER = re.compile(r"^(--- a/|\+\+\+ b/|@@ .* @@)", re.MULTILINE)

# JSON first char
_JSON_START = re.compile(r"^\s*[\[{]")

# Shebang
_SHEBANG = re.compile(r"^#!")

# Log line: leading timestamp + log level keyword
_LOG_LINE = re.compile(
    r"(?:"
    r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}"   # ISO timestamp
    r"|"
    r"\[?\d{2}[:/]\d{2}[:/]\d{2}\]?"              # HH:MM:SS
    r")"
    r".{0,40}"
    r"\b(?:INFO|WARN(?:ING)?|ERROR|DEBUG|FATAL|TRACE|CRITICAL)\b",
    re.IGNORECASE,
)

# Search result: path:lineno: content  (grep/rg style)
_SEARCH_LINE = re.compile(r"^[^\s:][^:]*:\d+[:\s]")

# Code keywords (per-line density check)
_CODE_KEYWORDS = re.compile(
    r"\b(?:import|from|def |class |function |const |let |var |return|if |else |"
    r"for |while |switch |case |elif |endif|public |private |protected |"
    r"static |void |int |str |bool |fn |func |package |use )\b"
)

# Language fingerprints for content-based detection (no fence)
_LANG_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("python",     re.compile(r"\bdef \w+\(|^from \w+ import |^import \w|class \w+\s*:", re.MULTILINE)),
    ("go",         re.compile(r"^package \w|^func \w+\(|^import \(", re.MULTILINE)),
    ("rust",       re.compile(r"\bfn \w+\(|let mut |^impl |^use \w", re.MULTILINE)),
    ("java",       re.compile(r"\bpublic class |\bprivate |\bprotected |\bpublic static void main\b")),
    ("typescript", re.compile(r"\b(const|let|var)\b\s+\w+\s*:\s*\w+|interface \w+\s*\{|export type |:\s*(string|number|boolean|any|void|never)\b")),
    ("javascript", re.compile(r"\b(const|let|var)\b|\bfunction\b|\b=>\b|\bexport\b|\brequire\s*\(")),
    ("css",        re.compile(r"^\s*[\w#.:\[*][^{]*\{\s*$", re.MULTILINE)),
    ("html",       re.compile(r"<(!DOCTYPE|html|head|body|div|span|p|a)\b", re.IGNORECASE)),
    ("sql",        re.compile(r"\b(SELECT|INSERT|UPDATE|DELETE|CREATE|DROP|ALTER|FROM|WHERE)\b", re.IGNORECASE)),
    ("yaml",       re.compile(r"^\w[\w\s]*:\s*\S", re.MULTILINE)),
]

# Fence language aliases → canonical name
_FENCE_LANG_MAP: dict[str, str] = {
    "py":         "python",
    "python":     "python",
    "python3":    "python",
    "js":         "javascript",
    "javascript": "javascript",
    "jsx":        "javascript",
    "ts":         "typescript",
    "typescript": "typescript",
    "tsx":        "typescript",
    "java":       "java",
    "go":         "go",
    "golang":     "go",
    "rs":         "rust",
    "rust":       "rust",
    "c":          "c",
    "cpp":        "cpp",
    "c++":        "cpp",
    "cxx":        "cpp",
    "rb":         "ruby",
    "ruby":       "ruby",
    "php":        "php",
    "sh":         "shell",
    "bash":       "shell",
    "shell":      "shell",
    "zsh":        "shell",
    "fish":       "shell",
    "sql":        "sql",
    "yaml":       "yaml",
    "yml":        "yaml",
    "toml":       "toml",
    "html":       "html",
    "css":        "css",
    "json":       "json",
    "xml":        "xml",
    "md":         "markdown",
    "markdown":   "markdown",
}

# Shebang interpreter → language
_SHEBANG_LANG: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"python"),  "python"),
    (re.compile(r"node|nodejs"), "javascript"),
    (re.compile(r"ruby"),    "ruby"),
    (re.compile(r"php"),     "php"),
    (re.compile(r"perl"),    "perl"),
    (re.compile(r"bash|sh|zsh|fish|dash"), "shell"),
    (re.compile(r"env\s+(\w+)"), None),  # handled specially below
]


# ---------------------------------------------------------------------------
# Detector
# ---------------------------------------------------------------------------

class ContentDetector:
    """Rule-based content type detector."""

    # -- Public API ----------------------------------------------------------

    def detect(self, text: str) -> DetectionResult:
        """Detect content type from text. Returns best match."""
        if not text or not text.strip():
            return DetectionResult("text", None, 0.5)

        # 1. Markdown code fence
        fence_result = self._check_code_fence(text)
        if fence_result is not None:
            return fence_result

        # 2. Diff headers
        if self._check_diff(text):
            return DetectionResult("diff", None, 0.95)

        # 3. JSON
        if self._check_json(text):
            return DetectionResult("json", None, 0.9)

        # 4. Shebang
        shebang_result = self._check_shebang(text)
        if shebang_result is not None:
            return shebang_result

        lines = text.splitlines()
        non_empty = [ln for ln in lines if ln.strip()]
        total = max(len(non_empty), 1)

        # 5. Log density
        log_hits = sum(1 for ln in non_empty if _LOG_LINE.search(ln))
        if log_hits / total > 0.30:
            return DetectionResult("log", None, 0.8)

        # 6. Search result density
        search_hits = sum(1 for ln in non_empty if _SEARCH_LINE.match(ln))
        if search_hits / total > 0.40:
            return DetectionResult("search", None, 0.8)

        # 7. Code keyword density
        kw_hits = sum(1 for ln in non_empty if _CODE_KEYWORDS.search(ln))
        if kw_hits / total > 0.15:
            lang = self.detect_language(text)
            return DetectionResult("code", lang, 0.7)

        return DetectionResult("text", None, 0.5)

    def detect_language(self, text: str) -> str | None:
        """Detect programming language from code text (no fence context)."""
        for lang, pattern in _LANG_PATTERNS:
            if pattern.search(text):
                return lang
        return None

    def detect_sections(self, text: str) -> list[Section]:
        """Split mixed content into typed sections (text interleaved with code fences)."""
        sections: list[Section] = []
        lines = text.splitlines(keepends=True)
        i = 0
        text_start = 0

        while i < len(lines):
            stripped = lines[i].rstrip("\n\r")
            m = _FENCE_OPEN.match(stripped)
            if m is None:
                i += 1
                continue

            # Flush preceding text block
            if i > text_start:
                block = "".join(lines[text_start:i])
                sections.append(self._classify_block(block, text_start + 1, i))

            fence_char = m.group(1)[0]
            raw_lang = m.group(2).strip().lower()
            lang = _FENCE_LANG_MAP.get(raw_lang) or (raw_lang or None)
            fence_start = i
            close_pat = _FENCE_CLOSE_BACKTICK if fence_char == "`" else _FENCE_CLOSE_TILDE

            i += 1
            while i < len(lines) and not close_pat.match(lines[i].rstrip("\n\r")):
                i += 1

            code_lines = lines[fence_start: i + 1]
            code_block = "".join(code_lines)
            sections.append(Section(
                content=code_block,
                content_type="code",
                language=lang,
                start_line=fence_start + 1,
                end_line=i + 1,
            ))
            i += 1
            text_start = i

        # Trailing text
        if text_start < len(lines):
            block = "".join(lines[text_start:])
            sections.append(self._classify_block(block, text_start + 1, len(lines)))

        return sections

    # -- Private helpers -----------------------------------------------------

    def _check_code_fence(self, text: str) -> DetectionResult | None:
        m = _FENCE_OPEN.search(text)
        if m is None:
            return None
        raw_lang = m.group(2).strip().lower()
        lang = _FENCE_LANG_MAP.get(raw_lang) or (raw_lang or None)
        return DetectionResult("code", lang, 0.95)

    def _check_diff(self, text: str) -> bool:
        matches = _DIFF_HEADER.findall(text)
        return len(matches) >= 2

    def _check_json(self, text: str) -> bool:
        stripped = text.strip()
        if not stripped or stripped[0] not in ("{", "["):
            return False
        try:
            json.loads(stripped)
            return True
        except (json.JSONDecodeError, ValueError):
            return False

    def _check_shebang(self, text: str) -> DetectionResult | None:
        first_line = text.split("\n", 1)[0]
        if not _SHEBANG.match(first_line):
            return None
        lang = self._lang_from_shebang(first_line)
        return DetectionResult("code", lang, 0.9)

    def _lang_from_shebang(self, shebang: str) -> str | None:
        for pattern, lang in _SHEBANG_LANG:
            m = pattern.search(shebang)
            if m:
                if lang is not None:
                    return lang
                # env case: look at captured interpreter name
                interpreter = m.group(1).lower() if m.lastindex else ""
                return _FENCE_LANG_MAP.get(interpreter, interpreter or None)
        return None

    def _classify_block(self, block: str, start_line: int, end_line: int) -> Section:
        result = self.detect(block)
        return Section(
            content=block,
            content_type=result.content_type,
            language=result.language,
            start_line=start_line,
            end_line=end_line,
        )
