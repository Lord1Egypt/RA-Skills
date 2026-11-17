from __future__ import annotations

import html
import re
from typing import Any

DEFAULT_CANNOT_START = frozenset(
    "，。；：！？、）》】”’」』〉〕〗〙〛）,.;:!?]}"
)
DEFAULT_CANNOT_END = frozenset("（《【“‘「『〈〔〖〘〚([{")
SINGLE_HAN_TAIL_PATTERN = re.compile(
    r"^[\u3400-\u9fff]["
    + re.escape("".join(DEFAULT_CANNOT_START))
    + r"]*$"
)
STATISTICAL_TOKEN_PATTERN = re.compile(
    r"(?<![\w])[-+−]?(?:\d+(?:\.\d+)?|\.\d+)(?:%|\*{1,3})?"
)
SIGNIFICANCE_PREFIX_PATTERN = re.compile(r"\*{1,3}p")


def reportlab_cjk_markup(
    text: str,
    *,
    cannot_start: frozenset[str] = DEFAULT_CANNOT_START,
    cannot_end: frozenset[str] = DEFAULT_CANNOT_END,
) -> str:
    """Escape text and add short ReportLab nobr groups for CJK kinsoku rules.

    The markup changes only line-breaking opportunities. It deliberately avoids
    invisible Unicode joiners because those can leak into the PDF text layer.
    """

    rendered_lines: list[str] = []
    for line in text.split("\n"):
        if not line:
            rendered_lines.append("")
            continue

        protected_boundaries = set()
        for pattern in (
            STATISTICAL_TOKEN_PATTERN,
            SIGNIFICANCE_PREFIX_PATTERN,
        ):
            protected_boundaries.update(
                boundary
                for match in pattern.finditer(line)
                for boundary in range(match.start(), match.end() - 1)
            )
        rendered: list[str] = []
        start = 0
        while start < len(line):
            end = start
            while end + 1 < len(line) and (
                line[end] in cannot_end
                or line[end + 1] in cannot_start
                or end in protected_boundaries
            ):
                end += 1

            chunk = html.escape(line[start : end + 1], quote=False)
            if end > start:
                chunk = f"<nobr>{chunk}</nobr>"
            rendered.append(chunk)
            start = end + 1
        rendered_lines.append("".join(rendered))

    return "<br/>".join(rendered_lines)


def _is_legal_cjk_boundary(left: Any, right: Any) -> bool:
    left_text = str(left)
    right_text = str(right)
    if not left_text or not right_text:
        return True
    if (
        left.frag is right.frag
        and getattr(left.frag, "nobr", False)
    ):
        return False
    if right_text[0] in DEFAULT_CANNOT_START:
        return False
    if left_text[-1] in DEFAULT_CANNOT_END:
        return False
    # 两侧都是半角字母数字时不算合法断点：拉丁词不能从中间断开。
    return not (
        ord(left_text[-1]) < 0x3000
        and ord(right_text[0]) < 0x3000
        and left_text[-1].isalnum()
        and right_text[0].isalnum()
    )


def _is_single_han_tail(glyphs: list[Any], start: int) -> bool:
    text = "".join(
        str(glyph)
        for glyph in glyphs[start:]
        if not hasattr(glyph.frag, "lineBreak")
    ).strip()
    return bool(SINGLE_HAN_TAIL_PATTERN.fullmatch(text))


def install_reportlab_cjk_nobr_patch() -> None:
    """Make ReportLab's CJK wrapper honor kinsoku and ``<nobr>`` fragments.

    ReportLab 5.0 parses ``<nobr>`` but its stock CJK splitter ignores the
    fragment flag. The replacement keeps the public Paragraph API unchanged
    and selects legal wrap-down boundaries without adding text characters.
    """

    from reportlab.platypus import paragraph

    if getattr(paragraph.cjkFragSplit, "_academic_pdf_kinsoku", False):
        return

    def glyph_width(glyph: Any, max_width: float) -> float:
        width = glyph.width
        if hasattr(width, "normalizedValue"):
            width._normalizer = max_width
            return float(width.normalizedValue(max_width))
        return float(width)

    def patched_cjk_frag_split(
        frags: list[Any],
        max_widths: float | list[float] | tuple[float, ...],
        calc_bounds: bool,
        encoding: str = "utf8",
    ) -> Any:
        if not isinstance(max_widths, (list, tuple)):
            max_widths = [max_widths]

        glyphs: list[Any] = []
        for frag in frags:
            text = frag.text
            if paragraph.isBytes(text):
                text = text.decode(encoding)
            if text:
                glyphs.extend(
                    paragraph.cjkU(char, frag, encoding)
                    for char in text
                )
            else:
                glyphs.append(paragraph.cjkU(text, frag, encoding))

        lines: list[Any] = []
        line_start = 0
        while line_start < len(glyphs):
            max_width = float(max_widths[min(len(lines), len(max_widths) - 1)])
            cursor = line_start
            used_width = 0.0
            explicit_break = False

            while cursor < len(glyphs):
                glyph = glyphs[cursor]
                if hasattr(glyph.frag, "lineBreak"):
                    cursor += 1
                    explicit_break = True
                    break
                width = glyph_width(glyph, max_width)
                if (
                    cursor > line_start
                    and used_width + width > max_width + paragraph._FUZZ
                ):
                    break
                used_width += width
                cursor += 1

            if explicit_break or cursor >= len(glyphs):
                break_at = cursor
                line_break = explicit_break
            else:
                break_at = cursor
                while (
                    break_at > line_start
                    and not _is_legal_cjk_boundary(
                        glyphs[break_at - 1],
                        glyphs[break_at],
                    )
                ):
                    break_at -= 1
                if break_at <= line_start:
                    break_at = max(line_start + 1, cursor)
                elif _is_single_han_tail(glyphs, break_at):
                    balanced_break = break_at - 1
                    while (
                        balanced_break > line_start
                        and not _is_legal_cjk_boundary(
                            glyphs[balanced_break - 1],
                            glyphs[balanced_break],
                        )
                    ):
                        balanced_break -= 1
                    if balanced_break > line_start:
                        break_at = balanced_break
                line_break = False

            segment = glyphs[line_start:break_at]
            segment_width = sum(
                glyph_width(glyph, max_width)
                for glyph in segment
                if not hasattr(glyph.frag, "lineBreak")
            )
            lines.append(
                paragraph.makeCJKParaLine(
                    segment,
                    max_width,
                    segment_width,
                    max_width - segment_width,
                    line_break,
                    calc_bounds,
                )
            )
            line_start = break_at

        return paragraph.ParaLines(kind=1, lines=lines)

    patched_cjk_frag_split._academic_pdf_kinsoku = True
    paragraph.cjkFragSplit = patched_cjk_frag_split
