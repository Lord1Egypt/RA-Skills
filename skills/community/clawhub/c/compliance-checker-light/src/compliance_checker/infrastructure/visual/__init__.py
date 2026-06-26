"""Visual inspection module - 视觉检测模块

基础设施层视觉检测组件，实现 Core 层 VisualCheckerProtocol 接口。
"""

from .qwen_client import QwenVLClient, VisualAPIError, ImageReadError
from .region_detector import (
    RegionDetector,
    TextRegion,
    PDFRegionDetector,
    PaddleOCRRegionDetector,
)
from .screenshot import (
    capture_page,
    capture_full_page_base64,
    capture_region_base64,
    get_page_size,
    get_page_count,
)

__all__ = [
    # QwenVL 客户端 - 实现 VisualCheckerProtocol
    "QwenVLClient",
    "VisualAPIError",
    "ImageReadError",
    # 区域检测器
    "RegionDetector",
    "TextRegion",
    "PDFRegionDetector",
    "PaddleOCRRegionDetector",
    # 截图工具
    "capture_page",
    "capture_full_page_base64",
    "capture_region_base64",
    "get_page_size",
    "get_page_count",
]
