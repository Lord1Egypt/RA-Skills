"""
图片解析器 - Infrastructure 层实现

实现 Core 层定义的 DocumentParserProtocol 接口。
支持 OCR 文字识别，所有异常转换为 ComplianceCheckerError。
"""

import logging
from pathlib import Path
from typing import Optional

from ...core.document import Document, DocumentMetadata, DocumentType, PageContent
from ...core.exceptions import DocumentParseError
from ...core.interfaces import DocumentParserProtocol, OCREngineProtocol

logger = logging.getLogger(__name__)

# 可选依赖：Pillow
try:
    from PIL import Image

    PIL_AVAILABLE = True
except ImportError:
    Image = None
    PIL_AVAILABLE = False


class ImageParser(DocumentParserProtocol):
    """
    图片文档解析器

    实现 DocumentParserProtocol 接口，提供图片文件的解析功能。
    功能包括：
    - 使用 OCR 提取图片中的文字内容
    - 提取图片元数据（尺寸、格式等）
    """

    SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}

    def __init__(
        self,
        ocr_engine: Optional[OCREngineProtocol] = None,
    ):
        """
        初始化图片解析器

        Args:
            ocr_engine: OCR 引擎实例（可选，通过依赖注入传入）

        Raises:
            DocumentParseError: Pillow 未安装
        """
        if not PIL_AVAILABLE:
            raise DocumentParseError("Pillow 未安装，请运行: pip install Pillow")

        self._ocr_engine = ocr_engine

    def parse(self, file_path: str) -> Document:
        """
        解析图片文件

        Args:
            file_path: 图片文件路径

        Returns:
            Document 对象

        Raises:
            DocumentParseError: 文件不存在、格式不支持或解析失败
        """
        path = Path(file_path)

        # 验证文件存在性
        if not path.exists():
            raise DocumentParseError(f"文件不存在: {file_path}")

        # 验证文件格式
        if path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise DocumentParseError(
                f"不支持的图片格式: {path.suffix}，"
                f"支持的格式: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        logger.info(f"开始解析图片: {file_path}")

        try:
            # 打开图片获取基本信息
            with Image.open(file_path) as img:
                width, height = img.size
                format_type = img.format
                mode = img.mode

            # 提取元数据
            metadata = DocumentMetadata(
                title=path.stem,
                custom={
                    "image_width": width,
                    "image_height": height,
                    "image_format": format_type,
                    "image_mode": mode,
                },
            )

            # 使用 OCR 提取文字
            ocr_text = self._extract_text_with_ocr(file_path)

            # 创建 Document 对象（图片视为单页文档）
            document = Document(
                path=str(path.absolute()),
                name=path.name,
                type=DocumentType.IMAGE,
                pages=1,
                pages_content=[
                    PageContent(
                        page_num=0,
                        text="",  # 图片无文本层
                        ocr_text=ocr_text,
                        has_text_layer=False,
                    )
                ],
                metadata=metadata,
            )

            logger.info(f"图片解析完成: {path.name}")
            return document

        except DocumentParseError:
            raise
        except Exception as e:
            raise DocumentParseError(f"图片解析失败: {e}") from e

    def _extract_text_with_ocr(self, file_path: str) -> str:
        """
        使用 OCR 引擎提取图片文字

        Args:
            file_path: 图片文件路径

        Returns:
            识别出的文字，如果 OCR 引擎不可用则返回空字符串
        """
        if self._ocr_engine is None:
            logger.warning("OCR 引擎未提供，无法识别图片文字")
            return ""

        try:
            return self._ocr_engine.recognize_image(file_path)
        except Exception as e:
            logger.error(f"OCR 识别失败: {e}")
            return ""


def parse_image(
    file_path: str,
    ocr_engine: Optional[OCREngineProtocol] = None,
) -> Document:
    """
    便捷函数：解析图片文件

    Args:
        file_path: 图片文件路径
        ocr_engine: OCR 引擎实例（可选）

    Returns:
        Document 对象

    Raises:
        DocumentParseError: 解析失败
    """
    parser = ImageParser(ocr_engine=ocr_engine)
    return parser.parse(file_path)
