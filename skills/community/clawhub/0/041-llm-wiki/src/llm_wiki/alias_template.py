"""别名通配符模板引擎(方案五;借鉴 ZotMoov `src/00-zotmoov-wildcard.js`)。

仅覆盖 `sources/zotero/` 别名命名;wiki 页面命名模板暂缓(页面名是
`[[链接]]` 体系的知识锚点,与文献管理式命名约束不同)。

支持的通配符:
- ``%a`` 主作者、``%y`` 年份、``%t`` 标题(空标题回退 "untitled")
- ``%c`` 分类层级路径(逐段清洗)、``%b`` CiteKey、``%T`` 条目类型
- ``%%%%`` 转义为字面 ``%``

所有替换值都经 ``sanitize_title_stem`` 清洗;模板字面值原样保留。
渲染结果保证为不含 ``..`` 段的相对路径。
"""

from __future__ import annotations

import re
from collections.abc import Mapping

from .sanitizer import sanitize_title_stem

_TOKEN = re.compile(r"%(.)", re.DOTALL)
_DASH_RUNS = re.compile(r"-{2,}")

# 简单通配符 → context 键(%t 空值回退 "untitled",其余空值渲染为空)
_SIMPLE_WILDCARDS = {
    "a": "author",
    "y": "year",
    "t": "title",
    "b": "citekey",
    "T": "item_type",
}


def _render_collection_path(raw: str) -> str:
    segments = [sanitize_title_stem(seg) for seg in raw.split("/") if seg.strip()]
    return "/".join(segments)


def render_alias_template(pattern: str, context: Mapping[str, str]) -> str:
    """把通配符模板渲染为 sources/zotero/ 下的相对别名路径(不含扩展名)。"""
    out: list[str] = []
    pos = 0
    for match in _TOKEN.finditer(pattern):
        out.append(pattern[pos : match.start()])
        code = match.group(1)
        if code == "%":
            out.append("%")
        elif code == "c":
            out.append(
                _render_collection_path(str(context.get("collection_path") or ""))
            )
        elif code in _SIMPLE_WILDCARDS:
            value = str(context.get(_SIMPLE_WILDCARDS[code]) or "").strip()
            if value:
                out.append(sanitize_title_stem(value))
            elif code == "t":
                out.append(sanitize_title_stem(""))
        else:
            raise ValueError(
                f"unknown wildcard %{code}; supported: %a %y %t %c %b %T and %%"
            )
        pos = match.end()
    out.append(pattern[pos:])

    segments: list[str] = []
    for segment in "".join(out).split("/"):
        cleaned = _DASH_RUNS.sub("-", segment).strip("-. ")
        if cleaned == "..":
            raise ValueError("alias template must not produce '..' path segments")
        if cleaned:
            segments.append(cleaned)
    return "/".join(segments)
