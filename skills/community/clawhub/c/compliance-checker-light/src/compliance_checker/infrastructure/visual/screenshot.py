"""截图工具 - PDF 页面截图

基础设施层组件，提供 PDF 页面截图功能。
"""

import logging
from typing import Optional, Tuple
from pathlib import Path
import tempfile

from ...core.exceptions import DocumentParseError

logger = logging.getLogger(__name__)

try:
    import fitz  # PyMuPDF

    HAS_FITZ = True
except ImportError:
    HAS_FITZ = False
    logger.warning("PyMuPDF not installed, screenshot functionality limited")


def capture_page(
    pdf_path: str,
    page_num: int = 0,
    dpi: int = 150,
    output_path: Optional[str] = None,
    bbox: Optional[Tuple[int, int, int, int]] = None,
) -> str:
    """
    截取 PDF 页面为图片

    Args:
        pdf_path: PDF 文件路径
        page_num: 页码（从0开始）
        dpi: 分辨率
        output_path: 输出路径（默认临时文件）
        bbox: 裁剪区域 (x1, y1, x2, y2)，None 表示整页

    Returns:
        截图文件路径

    Raises:
        DocumentParseError: 当 PyMuPDF 未安装或页面不存在时
    """
    if not HAS_FITZ:
        raise DocumentParseError("PyMuPDF required for screenshot capture")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise DocumentParseError(f"Failed to open PDF {pdf_path}: {e}") from e

    try:
        if page_num >= len(doc):
            raise DocumentParseError(f"Page {page_num} not found, document has {len(doc)} pages")

        page = doc[page_num]

        # 设置缩放矩阵
        mat = fitz.Matrix(dpi / 72, dpi / 72)

        # 如果有 bbox，裁剪；否则整页
        if bbox:
            rect = fitz.Rect(bbox)
            pix = page.get_pixmap(matrix=mat, clip=rect)
        else:
            pix = page.get_pixmap(matrix=mat)

        # 确定输出路径
        if output_path is None:
            suffix = f"_page{page_num}.png"
            fd, output_path = tempfile.mkstemp(suffix=suffix, prefix="compliance_")
            Path(output_path).write_bytes(pix.tobytes("png"))
        else:
            pix.save(output_path)

        return output_path

    finally:
        doc.close()


def capture_full_page_base64(pdf_path: str, page_num: int = 0, dpi: int = 150) -> str:
    """
    截取整页并转为 base64

    Args:
        pdf_path: PDF 文件路径
        page_num: 页码（从0开始）
        dpi: 分辨率

    Returns:
        base64 编码的 PNG 图片

    Raises:
        DocumentParseError: 当 PyMuPDF 未安装或页面不存在时
    """
    import base64
    import time

    output_path = capture_page(pdf_path, page_num, dpi)

    try:
        with open(output_path, "rb") as f:
            image_bytes = f.read()
        return base64.b64encode(image_bytes).decode("utf-8")
    finally:
        # 清理临时文件（带重试，Windows 可能文件锁定）
        for _ in range(3):
            try:
                Path(output_path).unlink(missing_ok=True)
                break
            except PermissionError:
                time.sleep(0.1)


def capture_region_base64(
    pdf_path: str,
    page_num: int = 0,
    bbox: Optional[Tuple[int, int, int, int]] = None,
    dpi: int = 150,
) -> str:
    """
    截取 PDF 指定区域并转为 base64

    Args:
        pdf_path: PDF 文件路径
        page_num: 页码（从0开始）
        bbox: 裁剪区域 (x1, y1, x2, y2)，None 表示整页
        dpi: 分辨率

    Returns:
        base64 编码的 PNG 图片

    Raises:
        DocumentParseError: 当 PyMuPDF 未安装或页面不存在时
    """
    import base64
    import time

    output_path = capture_page(pdf_path, page_num, dpi, bbox=bbox)

    try:
        with open(output_path, "rb") as f:
            image_bytes = f.read()
        return base64.b64encode(image_bytes).decode("utf-8")
    finally:
        # 清理临时文件（带重试，Windows 可能文件锁定）
        for _ in range(3):
            try:
                Path(output_path).unlink(missing_ok=True)
                break
            except PermissionError:
                time.sleep(0.1)


def get_page_size(pdf_path: str, page_num: int = 0) -> Tuple[int, int]:
    """
    获取页面尺寸

    Args:
        pdf_path: PDF 文件路径
        page_num: 页码（从0开始）

    Returns:
        (width, height) in points

    Raises:
        DocumentParseError: 当 PyMuPDF 未安装时
    """
    if not HAS_FITZ:
        raise DocumentParseError("PyMuPDF required")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise DocumentParseError(f"Failed to open PDF {pdf_path}: {e}") from e

    try:
        page = doc[page_num]
        rect = page.rect
        return (int(rect.width), int(rect.height))
    finally:
        doc.close()


def get_page_count(pdf_path: str) -> int:
    """
    获取 PDF 总页数

    Args:
        pdf_path: PDF 文件路径

    Returns:
        总页数

    Raises:
        DocumentParseError: 当 PyMuPDF 未安装时
    """
    if not HAS_FITZ:
        raise DocumentParseError("PyMuPDF required")

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        raise DocumentParseError(f"Failed to open PDF {pdf_path}: {e}") from e

    try:
        return len(doc)
    finally:
        doc.close()
