"""跨模块共用的枚举。

这些取值会写进作业数据并被检查，所以字面量必须稳定，改名等于破坏兼容。
"""

from __future__ import annotations

from enum import Enum


class QualityMode(str, Enum):
    """用户选的质量档位。

    它只表达"用户想要多快、多稳"，不表达"这篇 PDF 有多复杂"。
    版式复杂度是 :class:`Route` 的事，两者必须分开。
    """

    FAST = "fast"
    BALANCED = "balanced"
    PRECISE = "precise"

    @classmethod
    def parse(cls, value: object) -> QualityMode:
        text = str(value or "").strip().casefold()
        for member in cls:
            if member.value == text:
                return member
        legacy = LEGACY_REVIEW_MODE_TO_QUALITY_MODE.get(text)
        if legacy is not None:
            return legacy
        raise ValueError(
            "quality_mode 必须是 fast、balanced 或 precise，收到: "
            f"{value!r}"
        )


class Route(str, Enum):
    """这篇 PDF 应该怎么排版。与质量档位无关。"""

    STANDARD_AUTO = "standard-auto"
    HYBRID_COMPLEX_PAGES = "hybrid-complex-pages"
    CUSTOM_LAYOUT = "custom-layout"


class ElementType(str, Enum):
    """原文元素类型。"""

    DOCUMENT_TITLE = "document-title"
    AUTHOR_BLOCK = "author-block"
    AFFILIATION = "affiliation"
    PUBLICATION_METADATA = "publication-metadata"
    HEADING = "heading"
    BODY = "body"
    CAPTION = "caption"
    TABLE = "table"
    TABLE_NOTE = "table-note"
    RASTER_FIGURE = "raster-figure"
    VECTOR_FIGURE = "vector-figure"
    CHART = "chart"
    SCREENSHOT = "screenshot"
    DISPLAY_FORMULA = "display-formula"
    INLINE_FORMULA = "inline-formula"
    FOOTNOTE = "footnote"
    REFERENCE_HEADING = "reference-heading"
    REFERENCE_ENTRY = "reference-entry"
    HEADER = "header"
    FOOTER = "footer"
    PAGE_NUMBER = "page-number"
    WATERMARK = "watermark"
    UNKNOWN = "unknown"


#: 这些类型丢了就是丢内容，必须在候选里有对应产物。
REQUIRED_ELEMENT_TYPES = frozenset(
    {
        ElementType.DOCUMENT_TITLE,
        ElementType.AUTHOR_BLOCK,
        ElementType.AFFILIATION,
        ElementType.HEADING,
        ElementType.BODY,
        ElementType.CAPTION,
        ElementType.TABLE,
        ElementType.TABLE_NOTE,
        ElementType.RASTER_FIGURE,
        ElementType.VECTOR_FIGURE,
        ElementType.CHART,
        ElementType.SCREENSHOT,
        ElementType.DISPLAY_FORMULA,
        ElementType.FOOTNOTE,
        ElementType.REFERENCE_HEADING,
        ElementType.REFERENCE_ENTRY,
    }
)

#: 页面家具：可以合法省略，但省略必须有结构化代码。
PAGE_FURNITURE_TYPES = frozenset(
    {
        ElementType.HEADER,
        ElementType.FOOTER,
        ElementType.PAGE_NUMBER,
        ElementType.WATERMARK,
    }
)

#: 视觉元素：必须进图表清单。
VISUAL_ELEMENT_TYPES = frozenset(
    {
        ElementType.RASTER_FIGURE,
        ElementType.VECTOR_FIGURE,
        ElementType.CHART,
        ElementType.SCREENSHOT,
        ElementType.TABLE,
    }
)

#: 旧作业的 review.mode 到质量档位的映射。迁移只加字段，不删旧字段。
LEGACY_REVIEW_MODE_TO_QUALITY_MODE = {
    "none": QualityMode.FAST,
    "off": QualityMode.FAST,
    "independent": QualityMode.BALANCED,
    "on": QualityMode.BALANCED,
    "precise": QualityMode.PRECISE,
}

#: 质量档位反推 review.mode，供旧检查继续使用。
QUALITY_MODE_TO_REVIEW_MODE = {
    QualityMode.FAST: "none",
    QualityMode.BALANCED: "independent",
    QualityMode.PRECISE: "precise",
}
