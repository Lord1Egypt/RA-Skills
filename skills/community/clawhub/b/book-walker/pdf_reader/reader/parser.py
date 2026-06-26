"""PDF解析引擎 - PDF Reader"""
import logging
from pathlib import Path
from typing import List, Dict, Optional, Tuple, TYPE_CHECKING

import pdfplumber

from .blocks import BlockData, LineData, ImageData, PDFMetadata
from .exceptions import (
    PDFEncrypted, PDFCorrupted, PDFParseError,
    PDFPasswordError
)
from .text_enhance import enhance_text, is_scanned_pdf, extract_textsmart

if TYPE_CHECKING:
    from .cache import PDFCache

logger = logging.getLogger(__name__)

SCANNED_THRESHOLD = 0.8

# 内存中最多缓存的页数（按需加载、解析结果落盘，无总页数限制）
MAX_PAGES_IN_MEMORY = 5


class PDFParser:
    """PDF解析器 - 支持磁盘缓存与按需加载"""
    
    def __init__(self, pdf_path: str, cache: Optional["PDFCache"] = None):
        self.pdf_path = Path(pdf_path)
        self._cache = cache
        self._pdf = None
        self._metadata: Optional[PDFMetadata] = None
        self._pages_data: Dict[int, List[BlockData]] = {}
        self._global_block_count = 0
        self._global_line_count = 0
        self._page_offsets: Dict[int, int] = {}  # 页码 -> 该页首块的 block_id
        self._index_loaded = False  # 是否已从磁盘加载索引
        self._extract_mode: str = "text"  # text|ocr - 文本提取模式
    
    def set_extract_mode(self, mode: str):
        """设置文本提取模式
        
        切换模式时，清除当前页的缓存，确保用新模式重新解析
        """
        old_mode = self._extract_mode
        if mode in ("text", "ocr"):
            self._extract_mode = mode
            
            # 切换模式时，从内存缓存中清除当前页
            # 下次读取时会用新模式重新解析
            if old_mode != mode and self._pages_data:
                # 清除所有页的缓存，确保用新模式解析
                self._pages_data.clear()
    
    def get_current_page_data(self, page_num: int) -> List[BlockData]:
        """获取当前页数据，必要时重新解析"""
        return self.parse_page(page_num, force_reparse=True)
    
    def get_extract_mode(self) -> str:
        """获取当前文本提取模式"""
        return self._extract_mode
        
    def open(self) -> PDFMetadata:
        """打开PDF：优先使用磁盘缓存，无缓存时打开文件并提取元数据"""
        # 1. 尝试从磁盘加载索引（首次解析后已落盘）
        if self._cache and self._cache.has_cache(str(self.pdf_path)):
            index_data = self._cache.load_index(str(self.pdf_path))
            if index_data:
                self._metadata = PDFMetadata(
                    pdf_path=str(self.pdf_path),
                    total_pages=index_data["total_pages"],
                    total_blocks=index_data["total_blocks"],
                    has_toc=False,
                    is_scanned=index_data.get("is_scanned", False),
                    layout=index_data.get("layout", "single"),
                    index_generated=True
                )
                self._page_offsets = {
                    int(k): v for k, v in index_data.get("page_offsets", {}).items()
                }
                self._global_block_count = index_data["total_blocks"]
                self._index_loaded = True
                return self._metadata
        
        # 2. 无缓存：打开 PDF 并提取元数据
        try:
            self._pdf = pdfplumber.open(self.pdf_path)
        except Exception as e:
            if "encrypted" in str(e).lower():
                raise PDFEncrypted(f"PDF已加密: {self.pdf_path}")
            raise PDFCorrupted(f"PDF损坏或无法打开: {e}")
        
        is_scanned = self._detect_scanned()
        layout = self._detect_layout()
        
        self._metadata = PDFMetadata(
            pdf_path=str(self.pdf_path),
            total_pages=len(self._pdf.pages),
            total_blocks=0,
            has_toc=False,
            is_scanned=is_scanned,
            layout=layout,
            index_generated=False
        )
        return self._metadata
    
    def _detect_scanned(self) -> bool:
        """检测是否为扫描件"""
        if not self._pdf:
            return False
        
        image_pages = 0
        for page in self._pdf.pages:
            # 如果页面没有文本或文本极少，认为是图片页
            text = page.extract_text()
            if not text or len(text.strip()) < 50:
                image_pages += 1
        
        return (image_pages / len(self._pdf.pages)) > SCANNED_THRESHOLD
    
    def _detect_layout(self) -> str:
        """检测页面布局（单栏/多栏）"""
        if not self._pdf or len(self._pdf.pages) == 0:
            return "single"
        
        # 采样第一页分析
        sample_page = self._pdf.pages[0]
        chars = sample_page.chars
        
        if not chars:
            return "single"
        
        # 统计字符X坐标分布
        x_coords = [c['x0'] for c in chars]
        x_min, x_max = min(x_coords), max(x_coords)
        x_range = x_max - x_min
        
        # 简单判断：如果X坐标分布呈现多峰，可能为多栏
        # 这里用简化的方式：X坐标范围/页面宽度
        page_width = sample_page.width
        if x_range < page_width * 0.6:
            return "multi"  # 内容集中在左侧，可能是多栏
        
        return "single"
    
    def _ensure_pdf_open(self):
        """确保 PDF 已打开（按需加载时延迟打开）"""
        if self._pdf is not None:
            return
        if self._index_loaded:
            # 从缓存恢复，需要访问具体页时才打开 PDF
            self._pdf = pdfplumber.open(self.pdf_path)
    
    def parse_page(self, page_num: int, force_reparse: bool = False) -> List[BlockData]:
        """解析指定页：优先内存 -> 磁盘缓存 -> 实时解析
        
        Args:
            page_num: 页码
            force_reparse: 强制重新解析（忽略缓存），用于模式切换后
        """
        total_pages = self._metadata.total_pages if self._metadata else 0
        if page_num < 1 or page_num > total_pages:
            raise PDFParseError(f"页码无效: {page_num}")
        
        # 1. 内存缓存（如果不需要重新解析）
        if not force_reparse and page_num in self._pages_data:
            return self._pages_data[page_num]
        
        # 2. 磁盘缓存（如果不需要重新解析，且缓存是当前模式的）
        # 注意：模式切换后 force_reparse=True，会跳过磁盘缓存
        if not force_reparse and self._cache:
            disk_blocks = self._cache.load_page_from_disk(str(self.pdf_path), page_num)
            if disk_blocks:
                self._pages_data[page_num] = disk_blocks
                self._evict_page_if_needed()
                return disk_blocks
        
        # 3. 强制重新解析时，清除该页的磁盘缓存
        if force_reparse and self._cache:
            self._cache.delete_page(str(self.pdf_path), page_num)
        
        # 3. 实时解析
        self._ensure_pdf_open()
        if not self._pdf:
            raise PDFParseError("PDF未打开")
        
        self._page_offsets[page_num] = self._global_block_count
        page = self._pdf.pages[page_num - 1]
        
        # 根据提取模式选择方法
        if self._extract_mode == "ocr":
            blocks = self._extract_blocks_ocr(page, page_num)
        else:
            blocks = self._extract_blocks(page, page_num)
        self._pages_data[page_num] = blocks
        self._evict_page_if_needed()
        
        # 落盘
        if self._cache:
            self._cache.save_page_to_disk(str(self.pdf_path), page_num, blocks)
        
        return blocks
    
    def _evict_page_if_needed(self):
        """内存中页数过多时淘汰最久未用的页（简化版 FIFO）"""
        if len(self._pages_data) <= MAX_PAGES_IN_MEMORY:
            return
        # 淘汰第一页（按页码顺序，用于简单实现）
        pages = sorted(self._pages_data.keys())
        if len(pages) > MAX_PAGES_IN_MEMORY:
            del self._pages_data[pages[0]]
    
    def _extract_blocks(self, page, page_num: int) -> List[BlockData]:
        """从页面提取块 - 基于字符Y坐标分组"""
        blocks = []
        
        # 获取页面所有字符
        chars = page.chars
        if not chars:
            return blocks
        
        # 按Y坐标分组（行）
        # 同一行的字符Y坐标接近（容差3pt）
        y_tolerance = 3
        
        # 收集所有唯一的Y坐标（行）
        y_groups: Dict[float, List] = {}
        for char in chars:
            y = round(char['top'], 1)  # 取整到一位小数
            if y not in y_groups:
                y_groups[y] = []
            y_groups[y].append(char)
        
        # 按Y坐标排序
        sorted_ys = sorted(y_groups.keys())
        
        # 将相近的Y坐标合并（行间距处理）
        merged_rows: List[Tuple[float, List]] = []
        current_y = None
        current_row = []
        
        for y in sorted_ys:
            if current_y is None:
                current_y = y
                current_row = y_groups[y]
            elif abs(y - current_y) <= y_tolerance:
                # 合并到当前行
                current_row.extend(y_groups[y])
            else:
                # 保存当前行，开始新行
                merged_rows.append((current_y, current_row))
                current_y = y
                current_row = y_groups[y]
        
        # 保存最后一行
        if current_row:
            merged_rows.append((current_y, current_row))
        
        # 将行聚合成块（段落）
        current_block: Optional[BlockData] = None
        
        for y, row_chars in merged_rows:
            # 按X坐标排序字符
            row_chars.sort(key=lambda c: c['x0'])
            
            # 提取行的文本
            text = ''.join([c.get('text', '') for c in row_chars]).strip()
            if not text:
                continue
            
            # 获取字体信息
            font_name = row_chars[0].get('fontname', '')
            font_size = row_chars[0].get('size', 0)
            
            # 判断块类型
            block_type = self._detect_block_type(text, font_size, font_name)
            
            # 获取Y范围
            y0 = min([c['top'] for c in row_chars])
            y1 = max([c['bottom'] for c in row_chars])
            x0 = min([c['x0'] for c in row_chars])
            x1 = max([c['x1'] for c in row_chars])
            
            # 判断是否需要新建块
            if current_block is None:
                current_block = BlockData(
                    block_id=self._global_block_count,
                    page_idx=page_num,
                    type=block_type,
                    level=self._get_heading_level(font_size),
                    y0=y0,
                    y1=y1,
                    x0=x0,
                    x1=x1,
                    font_name=font_name,
                    font_size=font_size,
                    global_line_start=self._global_line_count
                )
            elif current_block.type == block_type and abs(current_block.y1 - y0) < 30:
                # 同一类型且行间距小（增大到30pt），继续当前块
                pass
            else:
                # 保存当前块，开始新块
                if current_block.lines:
                    blocks.append(current_block)
                    self._global_block_count += 1
                
                current_block = BlockData(
                    block_id=self._global_block_count,
                    page_idx=page_num,
                    type=block_type,
                    level=self._get_heading_level(font_size),
                    y0=y0,
                    y1=y1,
                    x0=x0,
                    x1=x1,
                    font_name=font_name,
                    font_size=font_size,
                    global_line_start=self._global_line_count
                )
            
            # 添加行（应用文本增强：修复连字问题）
            text = enhance_text(text)
            line_data = LineData(
                line_num=self._global_line_count + 1,
                text=text
            )
            current_block.lines.append(line_data)
            current_block.y1 = y1
            self._global_line_count += 1
        
        # 保存最后一个块
        if current_block and current_block.lines:
            blocks.append(current_block)
            self._global_block_count += 1
        
        # 提取图片
        self._extract_images(page, page_num, blocks)
        
        return blocks
    
    def _detect_block_type(self, text: str, font_size: float, font_name: str) -> str:
        """检测块类型"""
        # 标题检测：字号大 或者 文本较短且无标点
        if font_size > 12 or (len(text) < 50 and not ('.' in text or '，' in text)):
            return "heading"
        
        return "paragraph"
    
    def _get_heading_level(self, font_size: float) -> int:
        """根据字号判断标题级别"""
        if font_size >= 20:
            return 1
        elif font_size >= 16:
            return 2
        elif font_size >= 14:
            return 3
        return 4
    
    def _extract_blocks_ocr(self, page, page_num: int) -> List[BlockData]:
        """用 OCR 提取页面块（将页面转为图片后识别）"""
        import pypdfium2
        import subprocess
        import tempfile
        from pathlib import Path
        
        blocks = []
        pdf_path = str(self.pdf_path)
        
        try:
            # 1. 将页面转为图片 (使用 pypdfium2)
            pdf_doc = pypdfium2.PdfDocument(pdf_path)
            pdf_page = pdf_doc[page_num - 1]
            
            # 渲染页面为图片 (300 DPI = 4.166 scale)
            renderer = pdf_page.render(scale=300/72)
            pil_image = renderer.to_pil()
            
            # 保存临时图片
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                img_path = tmp.name
                pil_image.save(img_path)
            
            pdf_doc.close()
            
            # 2. OCR 识别 (使用 tesseract)
            result = subprocess.run(
                ["tesseract", img_path, "-", "-l", "eng"],
                capture_output=True,
                text=True,
                timeout=60
            )
            text = result.stdout
            
            # 清理临时文件
            Path(img_path).unlink(missing_ok=True)
            
            if not text.strip():
                return blocks
            
            # 3. 按行分割，生成块
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line = line.strip()
                if not line:
                    continue
                    
                # 创建块（每行一个块）
                block = BlockData(
                    block_id=self._global_block_count,
                    page_idx=page_num,
                    type="paragraph",
                    level=4,
                    y0=i * 10.0,
                    y1=(i + 1) * 10.0,
                    x0=0,
                    x1=500,
                    font_name="OCR",
                    font_size=10.0,
                    global_line_start=self._global_line_count
                )
                
                # 添加行
                from .blocks import LineData
                line_data = LineData(line_num=i + 1, text=line)
                block.lines.append(line_data)
                
                blocks.append(block)
                self._global_block_count += 1
                self._global_line_count += 1
            
            return blocks
            
        except FileNotFoundError:
            raise RuntimeError(
                "tesseract 未安装。请运行: brew install tesseract (macOS) 或 "
                "sudo apt install tesseract-ocr (Ubuntu)"
            )
        except Exception as e:
            logger.error(f"OCR 提取失败: {e}")
            return blocks
    
    def _extract_images(self, page, page_num: int, blocks: List[BlockData]):
        """提取页面图片并裁剪保存到缓存目录"""
        images = page.images
        if not images:
            return

        # 只在存在缓存管理器时生成图片目录
        img_dir = None
        if self._cache is not None:
            img_dir = self._cache.get_pdf_dir(str(self.pdf_path)) / "images"
            img_dir.mkdir(parents=True, exist_ok=True)

        page_image = None
        if img_dir is not None:
            try:
                page_image = page.to_image(resolution=150)
            except Exception:
                page_image = None

        # 将图片添加到对应Y位置的块，并在有能力时裁剪保存
        for img in images:
            y = img.get('top', 0)
            for block in blocks:
                if block.y0 <= y <= block.y1:
                    ref = f"p{page_num}_b{block.block_id}_img{len(block.images)}"
                    img_path = ""
                    if page_image is not None:
                        try:
                            bbox = (img.get('x0', 0), img.get('top', 0), img.get('x1', 0), img.get('bottom', 0))
                            cropped = page_image.crop(bbox)
                            out_path = img_dir / f"{ref}.png"
                            # PageImage.crop 返回 PageImage，提供 save 方法
                            cropped.save(str(out_path))
                            img_path = str(out_path)
                        except Exception:
                            img_path = ""

                    img_data = ImageData(
                        ref=ref,
                        x0=img.get('x0', 0),
                        y0=img.get('top', 0),
                        x1=img.get('x1', 0),
                        y1=img.get('bottom', 0),
                        width=int(img.get('width', 0)),
                        height=int(img.get('height', 0)),
                        path=img_path,
                    )
                    block.images.append(img_data)
                    break
    
    def get_block_by_global_id(self, block_id: int) -> Optional[Tuple[int, BlockData]]:
        """通过全局块ID获取块"""
        total_pages = self._metadata.total_pages if self._metadata else 0
        if total_pages == 0:
            return None
        
        # 根据 block_id 找到所在页（page_offsets[page] = 该页首块的 block_id）
        target_page = None
        for page_num in range(1, total_pages + 1):
            offset = self._page_offsets.get(page_num)
            if offset is None:
                # 该页尚未解析过，需解析以获取 offset
                self.parse_page(page_num)
                offset = self._page_offsets.get(page_num, 0)
            if block_id >= offset:
                target_page = page_num
        
        if target_page is None:
            return None
        
        offset = self._page_offsets.get(target_page, 0)
        blocks = self.parse_page(target_page)
        local_id = block_id - offset
        if 0 <= local_id < len(blocks):
            return target_page, blocks[local_id]
        return None
    
    def get_total_blocks(self) -> int:
        """获取总块数：有索引则直接返回，否则解析全部并落盘"""
        if self._index_loaded and self._metadata:
            return self._metadata.total_blocks
        
        self._ensure_pdf_open()
        if not self._pdf:
            return 0
        
        for page_num in range(1, len(self._pdf.pages) + 1):
            if page_num not in self._page_offsets:
                self.parse_page(page_num)
        
        # 首次解析完成，保存索引到磁盘
        if self._cache and self._metadata:
            index_data = {
                "total_pages": self._metadata.total_pages,
                "total_blocks": self._global_block_count,
                "page_offsets": {str(k): v for k, v in sorted(self._page_offsets.items())},
                "is_scanned": self._metadata.is_scanned,
                "layout": self._metadata.layout,
            }
            self._cache.save_index(str(self.pdf_path), index_data)
        
        return self._global_block_count
    
    def search(self, keyword: str, max_results: int = 20) -> List[Dict]:
        """搜索关键词，找到足够结果后提前终止以加速"""
        results = []
        total_pages = self._metadata.total_pages if self._metadata else 0
        if total_pages == 0 and self._pdf:
            total_pages = len(self._pdf.pages)
        if total_pages == 0:
            return results

        for page_num in range(1, total_pages + 1):
            if len(results) >= max_results:
                break
            blocks = self.parse_page(page_num)
            for block in blocks:
                for line in block.lines:
                    if keyword in line.text:
                        idx = line.text.find(keyword)
                        start = max(0, idx - 20)
                        end = min(len(line.text), idx + len(keyword) + 20)
                        snippet = "..." + line.text[start:end] + "..."
                        results.append({
                            "keyword": keyword,
                            "page": page_num,
                            "block_id": block.block_id,
                            "snippet": snippet
                        })
                        if len(results) >= max_results:
                            break
                if len(results) >= max_results:
                    break

        return results
    
    def close(self):
        """关闭PDF"""
        if self._pdf:
            self._pdf.close()
            self._pdf = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
