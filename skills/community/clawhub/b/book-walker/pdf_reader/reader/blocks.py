"""数据类 - PDF Reader"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import re


@dataclass
class LineData:
    """行数据类"""
    line_num: int
    text: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {"line_num": self.line_num, "text": self.text}
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "LineData":
        return cls(line_num=d["line_num"], text=d["text"])


@dataclass
class SentenceData:
    """句子数据类"""
    sentence_id: int
    text: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {"sentence_id": self.sentence_id, "text": self.text}
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "SentenceData":
        return cls(sentence_id=d["sentence_id"], text=d["text"])


class SentenceSplitter:
    """句子分割器 - 处理缩写和数字"""
    
    # 缩写白名单（不分割）
    ABBREVIATIONS = {
        'dr', 'mr', 'mrs', 'ms', 'prof', 'st',  # 人名
        'u.s', 'u.k', 'u.n', 'e.u',              # 国家
        'etc', 'eg', 'ie', 'vs', 'et al',        # 拉丁
        'fig', 'eq', 'sec', 'chap', 'no',        # 学术
        'jr', 'sr', 'inc', 'ltd', 'corp',        # 其他
        'a.m', 'p.m',
    }
    
    # 数字模式
    NUMBER_PATTERN = re.compile(r'\d+\.\d+')
    
    def split(self, text: str) -> List[str]:
        """分割文本为句子列表"""
        if not text:
            return []
        
        import re
        
        # 简化方案：直接匹配句子
        # 1. 先保护缩写（用占位符）
        # 2. 找到句子结束位置
        # 3. 恢复占位符
        
        # 1. 保护缩写：找到所有缩写位置，用占位符替换
        # 匹配 U.S., Dr., Fig., e.g., i.e., etc., et al. 等
        abbrev_patterns = [
            r'[A-Z]\.[A-Z]\.',  # U.S. U.K.
            r'[A-Z][a-z]+\.',  # Dr. Fig. etc.
            r'[a-z]\.[a-z]\.',  # e.g. i.e.
        ]
        
        abbrev_positions = []
        for pattern in abbrev_patterns:
            for m in re.finditer(pattern, text):
                abbrev_positions.append((m.start(), m.end()))
        
        # 按位置排序，合并重叠
        abbrev_positions.sort()
        
        # 用特殊标记替换缩写
        marked_text = ""
        last_end = 0
        abbrev_map = {}
        idx = 0
        for start, end in abbrev_positions:
            if start >= last_end:
                key = f"__ABBR{idx}__"
                abbrev_map[key] = text[start:end]
                marked_text += text[last_end:start] + key
                last_end = end
                idx += 1
        
        marked_text += text[last_end:]
        
        # 2. 按句子结束符分割
        sentences = []
        parts = re.split(r'(?<=[.!?])\s+', marked_text)
        
        for part in parts:
            # 恢复缩写
            for key, val in abbrev_map.items():
                part = part.replace(key, val)
            
            if part.strip():
                sentences.append(part.strip())
        
        return [s for s in sentences if s]
    
    def _is_abbreviation(self, text: str) -> bool:
        """检查是否是缩写"""
        text_lower = text.lower().strip()
        
        # 完全匹配
        if text_lower in self.ABBREVIATIONS:
            return True
        
        # 统一清理后比较
        text_clean = text_lower.replace('.', '').replace(' ', '')
        for abbr in self.ABBREVIATIONS:
            if abbr.replace('.', '').replace(' ', '') == text_clean:
                return True
        
        return False
    
    def _is_abbreviation(self, text: str) -> bool:
        """检查是否是缩写"""
        text_lower = text.lower().strip()
        
        # 完全匹配
        if text_lower in self.ABBREVIATIONS:
            return True
        
        # 统一清理后比较
        text_clean = text_lower.replace('.', '').replace(' ', '')
        for abbr in self.ABBREVIATIONS:
            if abbr.replace('.', '').replace(' ', '') == text_clean:
                return True
        
        return False


@dataclass
class ImageData:
    """图片数据类"""
    ref: str
    x0: float = 0
    y0: float = 0
    x1: float = 0
    y1: float = 0
    width: int = 0
    height: int = 0
    path: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "ref": self.ref,
            "bbox": {"x0": self.x0, "y0": self.y0, "x1": self.x1, "y1": self.y1},
            "width": self.width,
            "height": self.height,
            "path": self.path,
        }
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "ImageData":
        bbox = d.get("bbox", {})
        return cls(
            ref=d["ref"],
            x0=bbox.get("x0", 0),
            y0=bbox.get("y0", 0),
            x1=bbox.get("x1", 0),
            y1=bbox.get("y1", 0),
            width=d.get("width", 0),
            height=d.get("height", 0),
            path=d.get("path", ""),
        )


@dataclass
class BlockData:
    """块数据类"""
    block_id: int
    page_idx: int
    type: str = "paragraph"
    level: int = 0
    y0: float = 0
    y1: float = 0
    x0: float = 0
    x1: float = 0
    font_name: str = ""
    font_size: float = 0
    global_line_start: int = 0
    lines: List[LineData] = field(default_factory=list)
    images: List[ImageData] = field(default_factory=list)
    sentences: List[SentenceData] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "block_id": self.block_id,
            "page_idx": self.page_idx,
            "type": self.type,
            "level": self.level,
            "y_range": [self.y0, self.y1],
            "x_range": [self.x0, self.x1],
            "font": {"name": self.font_name, "size": self.font_size},
            "global_line_start": self.global_line_start,
            "lines": [l.to_dict() for l in self.lines],
            "images": [i.to_dict() for i in self.images],
            "sentences": [s.to_dict() for s in self.sentences]
        }
    
    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "BlockData":
        font = d.get("font", {}) or {}
        y_range = d.get("y_range", [0, 0])
        x_range = d.get("x_range", [0, 0])
        return cls(
            block_id=d["block_id"],
            page_idx=d["page_idx"],
            type=d.get("type", "paragraph"),
            level=d.get("level", 0),
            y0=y_range[0] if len(y_range) >= 1 else 0,
            y1=y_range[1] if len(y_range) >= 2 else 0,
            x0=x_range[0] if len(x_range) >= 1 else 0,
            x1=x_range[1] if len(x_range) >= 2 else 0,
            font_name=font.get("name", ""),
            font_size=font.get("size", 0),
            global_line_start=d.get("global_line_start", 0),
            lines=[LineData.from_dict(l) for l in d.get("lines", [])],
            images=[ImageData.from_dict(i) for i in d.get("images", [])],
            sentences=[SentenceData.from_dict(s) for s in d.get("sentences", [])]
        )
    
    def get_text(self) -> str:
        """获取块内所有文本"""
        return "\n".join([line.text for line in self.lines])
    
    def get_full_text(self) -> str:
        """获取带行号的完整文本"""
        return "\n".join([f"{line.line_num}. {line.text}" for line in self.lines])
    
    def parse_sentences(self):
        """解析块内的句子"""
        if self.sentences:  # 已经解析过
            return
        
        full_text = self.get_text().replace("\n", " ")
        splitter = SentenceSplitter()
        sent_list = splitter.split(full_text)
        
        self.sentences = [
            SentenceData(sentence_id=i, text=s)
            for i, s in enumerate(sent_list)
        ]


@dataclass
class PDFMetadata:
    """PDF元数据"""
    pdf_path: str
    total_pages: int = 0
    total_blocks: int = 0
    has_toc: bool = False
    is_scanned: bool = False
    layout: str = "single"
    index_generated: bool = False
    

@dataclass
class BookmarkData:
    """书签数据"""
    id: int
    page: int
    block_id: int
    note: str
    created_at: str
