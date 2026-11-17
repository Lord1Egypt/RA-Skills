"""字体分段与行内标记：纯文本处理，不碰 ReportLab 文档结构。

从 ``scripts/build_candidate.py`` 原样搬来，行为不变。搬出来的理由是
它们是**纯函数**：给定文本和字体名，输出标记字符串，不依赖排版上下文，
可以单独测试、单独读懂。

三件事：

- 上标字符与连字的归一（原文抽取常带出没有字形的连字）；
- 按字符判断字体覆盖，缺字形的片段切成独立段换字体；
- ReportLab 行内标记（CJK 禁则、上标、字体切换）。
"""

from __future__ import annotations

import html
import re
import unicodedata

from reportlab.pdfbase import pdfmetrics

from academic_pdf_translation.render.cjk_markup import (
    reportlab_cjk_markup,
)

SUPERSCRIPT_DIGITS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
#: C0 控制字符（保留换行与制表符），不得进入候选 PDF。
CONTROL_CHARACTER_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")
#: 排版连字（U+FB00 起）绝大多数字体都没有字形，抽文字时会变成空字符。
#: 原文抽取经常带出它们（例如 "Caﬀe"），这里统一还原成普通字母。
LIGATURE_REPLACEMENTS = {
    "\ufb00": "ff",
    "\ufb01": "fi",
    "\ufb02": "fl",
    "\ufb03": "ffi",
    "\ufb04": "ffl",
    "\ufb05": "st",
    "\ufb06": "st",
}


def _unicode_superscript_characters() -> str:
    characters = set(SUPERSCRIPT_DIGITS + "⁺⁻⁼⁽⁾")
    for start, end in ((0x2070, 0x209F), (0x1D2C, 0x1D6A)):
        for codepoint in range(start, end + 1):
            character = chr(codepoint)
            name = unicodedata.name(character, "")
            normalized = unicodedata.normalize("NFKC", character)
            if (
                (
                    "SUPERSCRIPT" in name
                    or name.startswith("MODIFIER LETTER SMALL")
                )
                and normalized != character
                and normalized
            ):
                characters.add(character)
    return "".join(sorted(characters, key=ord))


SUPERSCRIPT_CHARACTERS = _unicode_superscript_characters()
SUPERSCRIPT_PATTERN_CLASS = re.escape(SUPERSCRIPT_CHARACTERS)
CJK_FONT_RUN_PATTERN = re.compile(
    r"[\u2e80-\u2fff\u3000-\u303f\u3040-\u30ff"
    r"\u3100-\u318f\u31a0-\u31ef\u3400-\u4dbf"
    r"\u4e00-\u9fff\uac00-\ud7af\uf900-\ufaff"
    r"\uff00-\uffef]+"
)
MARKUP_TOKEN_PATTERN = re.compile(
    rf"([{SUPERSCRIPT_PATTERN_CLASS}]+|{CJK_FONT_RUN_PATTERN.pattern})"
)


def _plain_superscript(text: str) -> str:
    return "".join(
        unicodedata.normalize("NFKC", character)
        for character in text
    )


#: 本次构建的数学符号后备字体名；没有选出后备时为 None。
#: 正文/题录字体画不出的符号字符按字符段改用它（见 _markup）。
MATH_FALLBACK_FONT_NAME: str | None = None


def _font_supports(font_name: str, character: str) -> bool:
    """已注册字体能否画出这个字符；无法判断时按"能"处理，不误拦。"""

    try:
        face = pdfmetrics.getFont(font_name).face
    except Exception:
        return True
    mapping = getattr(face, "charToGlyph", None)
    if not isinstance(mapping, dict) or not mapping:
        return True
    return ord(character) in mapping


def _fallback_runs(
    token: str,
    primary_font: str,
    fallback_font: str,
) -> list[tuple[str, bool]]:
    """把 token 切成 (片段, 是否改用后备字体) 的连续段。

    题录用的是拉丁字体，但保留原文的公式片段里可能出现 ∈、Ω 这类
    拉丁字体没有的符号。这些字符在候选里会退化成 \x00，
    直接触发 NULL_CHARACTERS。这里逐字符判断，缺字形就换后备字体。
    """

    runs: list[tuple[str, bool]] = []
    for character in token:
        needs_fallback = not _font_supports(
            primary_font,
            character,
        ) and _font_supports(fallback_font, character)
        if runs and runs[-1][1] == needs_fallback:
            runs[-1] = (runs[-1][0] + character, needs_fallback)
        else:
            runs.append((character, needs_fallback))
    return runs


def _markup(
    text: str,
    *,
    cjk_font: str | None = None,
    primary_font: str | None = None,
) -> str:
    safe_text = re.sub(
        r"(?<=[A-Za-z0-9])\x00(?=[A-Za-z0-9])",
        "-",
        text,
    ).replace("\x00", "")
    # 原文抽取偶尔会带出 C0 控制字符（数学字体的定界符最常见）。
    # 它们在候选里没有可映射的字形，抽文字时会变成 \x00，直接触发
    # NULL_CHARACTERS 硬失败。在进排版之前一律去掉。
    safe_text = CONTROL_CHARACTER_RE.sub("", safe_text)
    for ligature, plain in LIGATURE_REPLACEMENTS.items():
        if ligature in safe_text:
            safe_text = safe_text.replace(ligature, plain)
    safe_text = (
        safe_text.replace("x\u0304", "x-bar")
        .replace("X\u0304", "X-bar")
        .replace("\u0302", "^")
    )
    safe_text = re.sub(
        rf"\^([{SUPERSCRIPT_PATTERN_CLASS}]+)",
        lambda match: "^"
        + _plain_superscript(match.group(1)),
        safe_text,
    )
    safe_text = safe_text.translate(
        str.maketrans(
            {
                "\u02d2": ",",
                "\u2010": "-",
                "\u2011": "-",
                "\u2012": "-",
                "\u204e": "*",
                "\u2217": "*",
                "\u2731": "*",
                "\ufb00": "ff",
                "\ufb01": "fi",
                "\ufb02": "fl",
                "\ufb03": "ffi",
                "\ufb04": "ffl",
                "\ufb05": "st",
                "\ufb06": "st",
            }
        )
    )
    rendered_lines: list[str] = []
    escaped_font = html.escape(cjk_font, quote=True) if cjk_font else None
    for line in safe_text.split("\n"):
        rendered_tokens: list[str] = []
        for token in MARKUP_TOKEN_PATTERN.split(line):
            if not token:
                continue
            if all(
                character in SUPERSCRIPT_CHARACTERS
                for character in token
            ):
                rendered_tokens.append(
                    f"<super>{_plain_superscript(token)}</super>"
                )
                continue
            # 数学符号后备：段落主字体画不出、后备字体画得出的字符，
            # 独立成段换字体。不做这一步它们会退化成空字符。
            if MATH_FALLBACK_FONT_NAME:
                base_font = primary_font or cjk_font or "AcademicUnifiedRegular"
                math_runs = _fallback_runs(
                    token, base_font, MATH_FALLBACK_FONT_NAME
                )
                if any(needs for _, needs in math_runs):
                    rendered_tokens.append(
                        "".join(
                            (
                                f'<font name="{MATH_FALLBACK_FONT_NAME}">'
                                f"{reportlab_cjk_markup(piece)}</font>"
                                if needs
                                else reportlab_cjk_markup(piece)
                            )
                            for piece, needs in math_runs
                        )
                    )
                    continue
            rendered = reportlab_cjk_markup(token)
            if escaped_font and CJK_FONT_RUN_PATTERN.fullmatch(token):
                rendered = (
                    f'<font name="{escaped_font}">{rendered}</font>'
                )
            elif escaped_font and primary_font:
                runs = _fallback_runs(token, primary_font, cjk_font or "")
                if any(needs for _, needs in runs):
                    rendered = "".join(
                        (
                            f'<font name="{escaped_font}">'
                            f"{reportlab_cjk_markup(piece)}</font>"
                            if needs
                            else reportlab_cjk_markup(piece)
                        )
                        for piece, needs in runs
                    )
            rendered_tokens.append(rendered)
        rendered_lines.append("".join(rendered_tokens))
    return "<br/>".join(rendered_lines)


def _edge_label_lines(label: str) -> list[str]:
    return [
        line.strip()
        for line in str(label or "").splitlines()
        if line.strip()
    ]

