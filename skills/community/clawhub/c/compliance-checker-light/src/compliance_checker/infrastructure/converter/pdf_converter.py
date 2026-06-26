"""
PDF 转换器实现

使用 PyMuPDF（fitz）将 PDF 文件转换为图片格式。
纯 Python 实现，无需依赖外部系统软件（如 Poppler）。
"""

import logging
from typing import List, Union
from io import BytesIO

from ...core.interfaces import PDFConverterProtocol

logger = logging.getLogger(__name__)


class PyMuPDFConverter(PDFConverterProtocol):
    """
    PyMuPDF PDF 转换器

    使用 PyMuPDF（fitz）库将 PDF 文件转换为 PNG 图片。
    支持文件路径或字节流作为输入。

    使用方式：
        converter = PyMuPDFConverter()
        images = await converter.convert_to_images("/path/to/file.pdf")
        # 或
        images = await converter.convert_to_images(pdf_bytes)
    """

    def __init__(self, zoom_factor: float = 2.0, dpi: int = 200):
        """
        初始化 PDF 转换器

        Args:
            zoom_factor: 渲染缩放因子，默认为 2.0 以保证印章和签名清晰度
            dpi: 渲染 DPI（仅作为参考，实际通过 zoom_factor 控制）
        """
        self.zoom_factor = zoom_factor
        self.dpi = dpi

    async def convert_to_images(self, file_path_or_bytes: Union[str, bytes]) -> List[bytes]:
        """
        将 PDF 转换为图片字节流列表（每页对应一张图）

        Args:
            file_path_or_bytes: PDF 文件路径或字节流

        Returns:
            图片字节流列表（PNG 格式），每页对应一个 bytes 对象

        Raises:
            ImportError: 如果 PyMuPDF 未安装
            ValueError: 如果 PDF 文件损坏或格式不正确
            FileNotFoundError: 如果文件路径不存在
        """
        try:
            import fitz  # PyMuPDF
        except ImportError as e:
            raise ImportError("PyMuPDF (fitz) 未安装，请运行: pip install pymupdf") from e

        images = []

        try:
            # 打开 PDF 文档
            if isinstance(file_path_or_bytes, bytes):
                # 从字节流打开
                doc = fitz.open(stream=file_path_or_bytes, filetype="pdf")
            else:
                # 从文件路径打开
                doc = fitz.open(file_path_or_bytes)

            # 使用 with 语法确保文档正确关闭
            with doc:
                total_pages = len(doc)
                logger.info(f"PDF 共 {total_pages} 页，开始转换为图片")

                # 创建放大矩阵以保证清晰度
                matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)

                for page_num in range(total_pages):
                    page = doc.load_page(page_num)

                    # 渲染页面为像素图
                    pix = page.get_pixmap(matrix=matrix)

                    # 转换为 PNG 字节流
                    img_bytes = pix.tobytes("png")
                    images.append(img_bytes)

                    logger.debug(f"第 {page_num + 1}/{total_pages} 页转换完成")

            logger.info(f"PDF 转换完成，共生成 {len(images)} 张图片")
            return images

        except Exception as e:
            logger.error(f"PDF 转换失败: {e}", exc_info=True)
            raise ValueError(f"PDF 转换失败: {str(e)}") from e

    def convert_to_images_sync(self, file_path_or_bytes: Union[str, bytes]) -> List[bytes]:
        """
        同步版本：将 PDF 转换为图片字节流列表

        在异步环境中应优先使用 convert_to_images 方法。
        此方法用于不支持异步的场景。

        Args:
            file_path_or_bytes: PDF 文件路径或字节流

        Returns:
            图片字节流列表（PNG 格式）
        """
        import asyncio

        try:
            loop = asyncio.get_running_loop()
            # 如果在事件循环中，使用 run_in_executor
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(self._convert_sync_impl, file_path_or_bytes)
                return future.result()
        except RuntimeError:
            # 不在事件循环中，直接调用
            return self._convert_sync_impl(file_path_or_bytes)

    def _convert_sync_impl(self, file_path_or_bytes: Union[str, bytes]) -> List[bytes]:
        """
        同步实现的内部方法
        """
        import fitz

        images = []

        if isinstance(file_path_or_bytes, bytes):
            doc = fitz.open(stream=file_path_or_bytes, filetype="pdf")
        else:
            doc = fitz.open(file_path_or_bytes)

        with doc:
            matrix = fitz.Matrix(self.zoom_factor, self.zoom_factor)

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(matrix=matrix)
                img_bytes = pix.tobytes("png")
                images.append(img_bytes)

        return images
