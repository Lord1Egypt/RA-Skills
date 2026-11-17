"""Language symbol extractors.

Regex-based, deliberately. A full parser (tree-sitter, the TS compiler API) is
heavier to install and run than the job needs: we want the *location* and the
one-line *signature* of a definition, not a full AST. Each extractor yields
Symbol records for one file's text. Precision over recall: better to miss an
exotic declaration than to fill the index with false symbols.
"""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Symbol:
    name: str
    kind: str  # function | class | method | const | interface | type
    signature: str  # the trimmed declaration line
    line: int  # 1-based
    lang: str


def _line_no(text: str, idx: int) -> int:
    return text.count("\n", 0, idx) + 1


def _sig(line: str) -> str:
    return line.strip().rstrip("{").rstrip().rstrip(":").strip()


# --- Python ---------------------------------------------------------------

_PY_DEF = re.compile(r"^([ \t]*)(?:async[ \t]+)?def[ \t]+(\w+)[ \t]*\(", re.M)
_PY_CLASS = re.compile(r"^([ \t]*)class[ \t]+(\w+)\b", re.M)


def extract_python(text: str) -> list[Symbol]:
    out: list[Symbol] = []
    for m in _PY_CLASS.finditer(text):
        out.append(Symbol(m.group(2), "class", _sig(_full_line(text, m.start())),
                          _line_no(text, m.start()), "python"))
    for m in _PY_DEF.finditer(text):
        indent = m.group(1)
        kind = "method" if indent else "function"
        out.append(Symbol(m.group(2), kind, _sig(_full_line(text, m.start())),
                          _line_no(text, m.start()), "python"))
    return out


# --- JavaScript / TypeScript ----------------------------------------------

_JS_FUNC = re.compile(r"^[ \t]*(?:export[ \t]+)?(?:default[ \t]+)?(?:async[ \t]+)?function[ \t*]+(\w+)", re.M)
_JS_CLASS = re.compile(r"^[ \t]*(?:export[ \t]+)?(?:default[ \t]+)?(?:abstract[ \t]+)?class[ \t]+(\w+)", re.M)
# const Foo = (..) => / const Foo = async (..) => / const Foo: T = (..) =>
_JS_ARROW = re.compile(
    r"^[ \t]*(?:export[ \t]+)?(?:const|let|var)[ \t]+(\w+)\s*[:=][^\n]*?=>", re.M
)
_TS_INTERFACE = re.compile(r"^[ \t]*(?:export[ \t]+)?interface[ \t]+(\w+)", re.M)
_TS_TYPE = re.compile(r"^[ \t]*(?:export[ \t]+)?type[ \t]+(\w+)\s*=", re.M)


def extract_jsts(text: str, lang: str = "ts") -> list[Symbol]:
    out: list[Symbol] = []
    seen: set[tuple[str, int]] = set()

    def add(name: str, kind: str, start: int):
        ln = _line_no(text, start)
        key = (name, ln)
        if key in seen:
            return
        seen.add(key)
        out.append(Symbol(name, kind, _sig(_full_line(text, start)), ln, lang))

    for m in _JS_CLASS.finditer(text):
        add(m.group(1), "class", m.start())
    for m in _JS_FUNC.finditer(text):
        add(m.group(1), "function", m.start())
    for m in _JS_ARROW.finditer(text):
        add(m.group(1), "function", m.start())
    for m in _TS_INTERFACE.finditer(text):
        add(m.group(1), "interface", m.start())
    for m in _TS_TYPE.finditer(text):
        add(m.group(1), "type", m.start())
    return out


def _full_line(text: str, idx: int) -> str:
    start = text.rfind("\n", 0, idx) + 1
    end = text.find("\n", idx)
    if end == -1:
        end = len(text)
    return text[start:end]


# --- dispatch -------------------------------------------------------------

EXT_LANG = {
    ".py": "python",
    ".js": "js", ".jsx": "js", ".mjs": "js", ".cjs": "js",
    ".ts": "ts", ".tsx": "ts",
}


def extract(path: str, text: str) -> list[Symbol]:
    import os
    ext = os.path.splitext(path)[1].lower()
    lang = EXT_LANG.get(ext)
    if lang == "python":
        return extract_python(text)
    if lang in ("js", "ts"):
        return extract_jsts(text, lang)
    return []
