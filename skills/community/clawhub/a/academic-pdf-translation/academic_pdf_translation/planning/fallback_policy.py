"""安全降级：复杂内容重建不了的时候，宁可保守，也不能丢信息。

三级降级，逐级放弃"好看"，但一级都不放弃"完整"：

1. 按正常策略生成。
2. 保留原始元素区域，再附中文标签或中文说明。
3. 保留整张原文页面，另配一页中文阅读页。

第三级不漂亮。但它不会让读者拿到一份消失了图、压平了表格的 PDF。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from academic_pdf_translation.contracts.enums import ElementType
from academic_pdf_translation.planning.mode_policy import (
    FALLBACK_PRESERVE_ELEMENT_REGION,
    FALLBACK_PRESERVE_FULL_PAGE,
    ModePolicy,
)

LEVEL_PRIMARY = 1
LEVEL_PRESERVE_ELEMENT = 2
LEVEL_PRESERVE_PAGE = 3


@dataclass(frozen=True)
class FallbackChain:
    """一个元素的降级链。"""

    element_id: str
    levels: tuple[str, ...]
    reason: str = ""

    def next_after(self, strategy: str) -> str | None:
        """当前策略失败后该换成什么。"""

        try:
            index = self.levels.index(strategy)
        except ValueError:
            return self.levels[LEVEL_PRESERVE_ELEMENT - 1] if self.levels else None
        if index + 1 >= len(self.levels):
            return None
        return self.levels[index + 1]

    def as_dict(self) -> dict[str, Any]:
        return {
            "element_id": self.element_id,
            "levels": list(self.levels),
            "reason": self.reason,
        }


#: 这些类型必须有完整的三级降级：它们最容易在重建时丢内容。
COMPLEX_TYPES = frozenset(
    {
        ElementType.TABLE,
        ElementType.VECTOR_FIGURE,
        ElementType.CHART,
        ElementType.DISPLAY_FORMULA,
        ElementType.SCREENSHOT,
        ElementType.RASTER_FIGURE,
    }
)


def build_chain(
    element_id: str,
    element_type: ElementType,
    primary: str,
    policy: ModePolicy,
) -> FallbackChain:
    """给一个元素造降级链。"""

    if element_type not in COMPLEX_TYPES:
        # 普通文字降不到"保留原页"，它本来就不会丢结构。
        return FallbackChain(
            element_id=element_id,
            levels=(primary,),
            reason="普通文本元素不需要区域级降级",
        )
    levels = [primary]
    if primary != FALLBACK_PRESERVE_ELEMENT_REGION:
        levels.append(FALLBACK_PRESERVE_ELEMENT_REGION)
    levels.append(FALLBACK_PRESERVE_FULL_PAGE)
    return FallbackChain(
        element_id=element_id,
        levels=tuple(levels),
        reason=(
            f"复杂元素三级降级；栅格化保留时不低于 "
            f"{policy.preserved_region_min_dpi} DPI"
        ),
    )
