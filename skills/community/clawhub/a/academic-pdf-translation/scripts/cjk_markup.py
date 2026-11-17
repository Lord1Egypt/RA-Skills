"""兼容入口：CJK 行内标记已移入 academic_pdf_translation.render.cjk_markup。

保留这个路径，旧的 `from cjk_markup import ...` 继续可用。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from academic_pdf_translation.render.cjk_markup import (  # noqa: E402,F401
    DEFAULT_CANNOT_END,
    DEFAULT_CANNOT_START,
    SIGNIFICANCE_PREFIX_PATTERN,
    SINGLE_HAN_TAIL_PATTERN,
    STATISTICAL_TOKEN_PATTERN,
    _is_legal_cjk_boundary,
    _is_single_han_tail,
    install_reportlab_cjk_nobr_patch,
    reportlab_cjk_markup,
)
