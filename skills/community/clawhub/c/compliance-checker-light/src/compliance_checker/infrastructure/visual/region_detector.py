"""基于 OCR 的区域定位 - 用于视觉检查前定位大概区域

基础设施层组件，提供文本区域检测功能。
"""

import logging
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TextRegion:
    """文本区域数据类"""

    text: str
    bbox: Tuple[int, int, int, int]  # x1, y1, x2, y2
    page: int = 0
    confidence: float = 1.0


class PaddleOCRRegionDetector:
    """基于 PaddleOCR 的区域检测器"""

    def __init__(self):
        self._ocr = None

    def _get_ocr(self):
        """延迟初始化 PaddleOCR"""
        if self._ocr is None:
            try:
                from paddleocr import PaddleOCR

                # PaddleOCR 3.x API
                self._ocr = PaddleOCR(
                    lang="ch",
                    device="cpu",
                    use_textline_orientation=False,
                    use_doc_orientation_classify=False,
                    use_doc_unwarping=False,
                )
                logger.info("PaddleOCR 初始化成功")
            except ImportError:
                logger.error("PaddleOCR 未安装，请运行: pip install paddleocr")
                raise
        return self._ocr

    def detect_regions(self, image_path: str, page: int = 0) -> List[Dict]:
        """
        使用 PaddleOCR 检测图片中的文本区域

        Args:
            image_path: 图片文件路径
            page: 页码（用于标记来源）

        Returns:
            区域列表，每项包含 text, bbox, confidence, page
        """
        ocr = self._get_ocr()

        try:
            # PaddleOCR 3.x 使用 predict 方法
            result = ocr.predict(image_path)

            regions = []
            if result:
                # PaddleOCR 3.x 返回格式: 列表包含字典
                for item in result:
                    rec_texts = item.get("rec_texts", [])
                    rec_scores = item.get("rec_scores", [])
                    rec_polys = item.get("rec_polys", [])

                    for i, text in enumerate(rec_texts):
                        if i < len(rec_polys):
                            poly = rec_polys[i]  # [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
                            confidence = rec_scores[i] if i < len(rec_scores) else 1.0

                            # 转换为标准 bbox 格式 [x1, y1, x2, y2]
                            x1 = min(p[0] for p in poly)
                            y1 = min(p[1] for p in poly)
                            x2 = max(p[0] for p in poly)
                            y2 = max(p[1] for p in poly)

                            regions.append(
                                {
                                    "text": text,
                                    "bbox": [int(x1), int(y1), int(x2), int(y2)],
                                    "confidence": confidence,
                                    "page": page,
                                }
                            )

            return regions

        except Exception as e:
            logger.error(f"PaddleOCR 检测失败: {e}")
            return []

    def locate_keyword(
        self, image_path: str, keyword: str, page: int = 0, margin: int = 100
    ) -> Optional[Dict]:
        """
        在图片中定位关键词区域

        Args:
            image_path: 图片文件路径
            keyword: 要搜索的关键词
            page: 页码
            margin: 扩大区域的边距

        Returns:
            {
                "page": int,
                "bbox": [x1, y1, x2, y2],
                "text": str
            }
        """
        regions = self.detect_regions(image_path, page)

        keyword_lower = keyword.lower()

        for region in regions:
            text = region["text"]
            # 模糊匹配
            if keyword_lower in text.lower() or self._fuzzy_match(keyword, text):
                bbox = region["bbox"]
                # 扩大区域
                expanded_bbox = [
                    max(0, bbox[0] - margin),
                    max(0, bbox[1] - margin),
                    bbox[2] + margin,
                    bbox[3] + margin,
                ]

                return {"page": page, "bbox": expanded_bbox, "text": text}

        return None

    def _fuzzy_match(self, search: str, text: str) -> bool:
        """模糊匹配文本"""
        if not search or not text:
            return False

        search = search.lower()
        text = text.lower()

        # 简单实现：检查是否有部分匹配
        search_len = len(search)
        if search_len < 3:
            return search in text

        # 检查前一半字符是否匹配
        half_len = search_len // 2
        return search[:half_len] in text or search[-half_len:] in text


class RegionDetector:
    """基于 OCR 结果的区域检测器"""

    def __init__(self, ocr_results: Optional[List[Dict]] = None):
        """
        Args:
            ocr_results: OCR 结果列表，每项包含 text, bbox, page 等
        """
        self.regions: List[TextRegion] = []
        if ocr_results:
            self.regions = self._parse_ocr_results(ocr_results)

    def _parse_ocr_results(self, ocr_results: List[Dict]) -> List[TextRegion]:
        """解析 OCR 结果为 TextRegion 列表"""
        regions = []
        for item in ocr_results:
            if isinstance(item, dict):
                region = TextRegion(
                    text=item.get("text", ""),
                    bbox=tuple(item.get("bbox", [0, 0, 0, 0])),
                    page=item.get("page", 0),
                    confidence=item.get("confidence", 1.0),
                )
                regions.append(region)
        return regions

    def search(self, keyword: str, fuzzy: bool = True) -> List[TextRegion]:
        """
        搜索关键词定位区域

        Args:
            keyword: 搜索关键词
            fuzzy: 是否模糊匹配

        Returns:
            匹配的区域列表
        """
        matches = []
        keyword_lower = keyword.lower()

        for region in self.regions:
            text_lower = region.text.lower()

            if fuzzy:
                # 模糊匹配：包含关系
                if keyword_lower in text_lower or text_lower in keyword_lower:
                    matches.append(region)
            else:
                # 精确匹配
                if keyword_lower == text_lower:
                    matches.append(region)

        # 按置信度排序
        matches.sort(key=lambda r: r.confidence, reverse=True)
        return matches

    def expand_region(
        self, region: TextRegion, margin: int = 100, page_width: int = 0, page_height: int = 0
    ) -> Tuple[int, int, int, int]:
        """
        扩大区域范围（用于截图）

        Args:
            region: 原始区域
            margin: 边距（像素）
            page_width: 页面宽度（用于边界限制）
            page_height: 页面高度（用于边界限制）

        Returns:
            扩大后的 bbox (x1, y1, x2, y2)
        """
        x1, y1, x2, y2 = region.bbox

        # 扩大边距
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = x2 + margin
        y2 = y2 + margin

        # 限制在页面范围内
        if page_width > 0:
            x2 = min(x2, page_width)
        if page_height > 0:
            y2 = min(y2, page_height)

        return (x1, y1, x2, y2)

    def find_context_region(
        self, context_keywords: List[str], target_keyword: str, max_distance: int = 200
    ) -> Optional[TextRegion]:
        """
        在上下文关键词附近查找目标关键词

        例如：在"法定代表人"附近查找"签字"

        Args:
            context_keywords: 上下文关键词列表（如 ["法定代表人", "负责人"]）
            target_keyword: 目标关键词（如 "签字"）
            max_distance: 最大距离（像素）

        Returns:
            找到的目标区域，或 None
        """
        # 先找上下文区域
        context_regions = []
        for kw in context_keywords:
            matches = self.search(kw, fuzzy=True)
            context_regions.extend(matches)

        if not context_regions:
            return None

        # 在上下文区域附近找目标
        target_matches = self.search(target_keyword, fuzzy=True)

        for target in target_matches:
            for context in context_regions:
                # 检查是否在同一页
                if target.page != context.page:
                    continue

                # 计算中心点距离
                target_center = (
                    (target.bbox[0] + target.bbox[2]) / 2,
                    (target.bbox[1] + target.bbox[3]) / 2,
                )
                context_center = (
                    (context.bbox[0] + context.bbox[2]) / 2,
                    (context.bbox[1] + context.bbox[3]) / 2,
                )

                distance = (
                    (target_center[0] - context_center[0]) ** 2
                    + (target_center[1] - context_center[1]) ** 2
                ) ** 0.5

                if distance <= max_distance:
                    return target

        # 如果没找到附近的，返回第一个匹配的目标
        return target_matches[0] if target_matches else None


class PDFRegionDetector:
    """基于 PyMuPDF 的 PDF 区域检测器"""

    def __init__(self):
        self._fitz = None
        try:
            import fitz

            self._fitz = fitz
        except ImportError:
            logger.error("PyMuPDF not installed, PDFRegionDetector will not work")

    def is_available(self) -> bool:
        """检查是否可用"""
        return self._fitz is not None

    def locate_by_text(
        self, pdf_path: str, search_text: str, page_hint: Optional[int] = None, margin: int = 100
    ) -> Optional[Dict]:
        """
        在 PDF 中通过文本定位区域

        Args:
            pdf_path: PDF 文件路径
            search_text: 要搜索的文本
            page_hint: 建议查找的页码（可选）
            margin: 扩大区域的边距

        Returns:
            {
                "page": int,
                "bbox": [x1, y1, x2, y2],
                "text": str
            }
        """
        if not self._fitz:
            logger.error("PyMuPDF not available")
            return None

        try:
            doc = self._fitz.open(pdf_path)

            # 确定搜索范围
            if page_hint is not None and 0 <= page_hint < len(doc):
                pages_to_search = [page_hint]
            else:
                pages_to_search = range(len(doc))

            for page_num in pages_to_search:
                page = doc[page_num]

                # 获取页面文本块
                text_blocks = page.get_text("blocks")

                for block in text_blocks:
                    block_text = block[4]  # 文本内容

                    # 模糊匹配
                    if search_text in block_text or self._fuzzy_match(search_text, block_text):
                        bbox = list(block[:4])  # [x1, y1, x2, y2]

                        # 扩大区域（添加边距）
                        expanded_bbox = self._expand_bbox(bbox, page.rect, margin)

                        doc.close()
                        return {
                            "page": page_num,
                            "bbox": expanded_bbox,
                            "text": block_text[:200],  # 前200字符
                        }

            doc.close()
            return None

        except Exception as e:
            logger.error(f"PDF region detection failed: {e}")
            return None

    def _fuzzy_match(self, search: str, text: str) -> bool:
        """模糊匹配文本"""
        if not search or not text:
            return False

        search = search.lower()
        text = text.lower()

        # 简单实现：检查是否有部分匹配
        search_len = len(search)
        if search_len < 3:
            return search in text

        # 检查前一半字符是否匹配
        half_len = search_len // 2
        return search[:half_len] in text or search[-half_len:] in text

    def _expand_bbox(self, bbox: List[float], page_rect, margin: int = 100) -> List[float]:
        """扩大边界框"""
        x1, y1, x2, y2 = bbox

        # 添加边距
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(page_rect.width, x2 + margin)
        y2 = min(page_rect.height, y2 + margin)

        return [x1, y1, x2, y2]
