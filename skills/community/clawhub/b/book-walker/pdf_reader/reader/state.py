"""状态管理 - PDF Reader"""
import json
import time
from pathlib import Path
from typing import List, Optional, Dict, Any, TYPE_CHECKING
from dataclasses import dataclass, asdict

from .blocks import BookmarkData

if TYPE_CHECKING:
    from .cache import PDFCache


@dataclass
class ReadingState:
    """阅读状态"""
    pdf_path: Optional[str] = None
    current_page: int = 1
    current_block_idx: int = 0
    current_line_idx: int = 0
    current_sentence_idx: int = 0  # 句子索引
    mode: str = "sentence"  # sentence|block
    extract_mode: str = "text"  # text|ocr - 文本提取模式
    total_pages: int = 0
    total_blocks: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "current_page": self.current_page,
            "current_block_idx": self.current_block_idx,
            "current_line_idx": self.current_line_idx,
            "current_sentence_idx": self.current_sentence_idx,
            "mode": self.mode,
            "extract_mode": self.extract_mode,
            "total_pages": self.total_pages,
            "total_blocks": self.total_blocks
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReadingState':
        mode_value = data.get("mode", "sentence")
        if mode_value not in ("sentence",):
            mode_value = "sentence"
        extract_mode = data.get("extract_mode", "text")
        if extract_mode not in ("text", "ocr"):
            extract_mode = "text"
        return cls(
            pdf_path=data.get("pdf_path"),
            current_page=data.get("current_page", 1),
            current_block_idx=data.get("current_block_idx", 0),
            current_line_idx=data.get("current_line_idx", 0),
            current_sentence_idx=data.get("current_sentence_idx", 0),
            mode=mode_value,
            extract_mode=extract_mode,
            total_pages=data.get("total_pages", 0),
            total_blocks=data.get("total_blocks", 0)
        )


class StateManager:
    """状态管理器 - 支持按 PDF 切换存储目录（解析结果、进度、书签分目录保存）"""
    
    def __init__(self, storage_dir: str = None):
        # 与 PDFCache 保持一致，使用 ~/.cache/deep-reading/
        self._base_storage = Path(storage_dir) if storage_dir else Path.home() / ".cache" / "deep-reading"
        self._active_storage_dir: Optional[Path] = None
        
        self._state = ReadingState()
        self._bookmarks: List[BookmarkData] = []
        self._history: List[Dict] = []
        self._redo_stack: List[Dict] = []
    
    def switch_to_pdf(self, pdf_path: str, cache: "PDFCache"):
        """切换到指定 PDF 的专属目录，并从该目录加载进度和书签"""
        self._active_storage_dir = cache.get_pdf_dir(pdf_path)
        self._load_state()
        self._load_bookmarks()
    
    def clear_active_pdf(self):
        """清除当前 PDF 的激活状态（关闭 PDF 后调用）"""
        self._active_storage_dir = None
        self._state = ReadingState()
        self._bookmarks = []
        self._history.clear()
        self._redo_stack.clear()
    
    @property
    def _storage_dir(self) -> Path:
        return self._active_storage_dir if self._active_storage_dir else self._base_storage
    
    @property
    def state_file(self) -> Path:
        return self._storage_dir / "state.json"
    
    @property
    def bookmarks_file(self) -> Path:
        return self._storage_dir / "bookmarks.json"
    
    def _load_state(self):
        """加载状态"""
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._state = ReadingState.from_dict(data)
            except Exception:
                self._state = ReadingState()
        else:
            self._state = ReadingState()
    
    def _save_state(self):
        """保存状态"""
        with open(self.state_file, 'w', encoding='utf-8') as f:
            json.dump(self._state.to_dict(), f, ensure_ascii=False, indent=2)
    
    def _load_bookmarks(self):
        """加载书签"""
        if self.bookmarks_file.exists():
            try:
                with open(self.bookmarks_file, 'r', encoding='utf-8') as f:
                    self._bookmarks = [BookmarkData(**b) for b in json.load(f)]
            except Exception:
                self._bookmarks = []
        else:
            self._bookmarks = []
    
    def _save_bookmarks(self):
        """保存书签"""
        with open(self.bookmarks_file, 'w', encoding='utf-8') as f:
            json.dump([asdict(b) for b in self._bookmarks], f, ensure_ascii=False, indent=2)
    
    # === 状态操作 ===
    
    def get_state(self) -> ReadingState:
        return self._state
    
    def set_pdf(self, pdf_path: str, total_pages: int, total_blocks: int, first_block_id: int = 0):
        """设置PDF"""
        self._state.pdf_path = pdf_path
        self._state.current_page = 1
        self._state.current_block_idx = first_block_id
        self._state.current_line_idx = 0
        self._state.total_pages = total_pages
        self._state.total_blocks = total_blocks
        self._history.clear()
        self._redo_stack.clear()
        self._save_state()
    
    def update_position(self, page: int, block_idx: int, line_idx: int = 0, sentence_idx: int = 0):
        """更新阅读位置"""
        # 保存当前位置到历史
        self._history.append({
            "page": self._state.current_page,
            "block_idx": self._state.current_block_idx,
            "line_idx": self._state.current_line_idx,
            "sentence_idx": self._state.current_sentence_idx,
            "timestamp": time.time()
        })
        
        # 清除前进栈
        self._redo_stack.clear()
        
        # 更新位置
        self._state.current_page = page
        self._state.current_block_idx = block_idx
        self._state.current_line_idx = line_idx
        self._state.current_sentence_idx = sentence_idx
        self._save_state()
    
    def set_mode(self, mode: str):
        """设置阅读模式"""
        self._state.mode = mode
        self._save_state()
    
    def can_go_back(self) -> bool:
        """是否能后退"""
        return len(self._history) > 0
    
    def can_go_forward(self) -> bool:
        """是否能前进"""
        return len(self._redo_stack) > 0
    
    def go_back(self) -> Optional[Dict]:
        """后退"""
        if not self._history:
            return None
        
        # 保存当前位置到前进栈
        self._redo_stack.append({
            "page": self._state.current_page,
            "block_idx": self._state.current_block_idx,
            "line_idx": self._state.current_line_idx
        })
        
        # 恢复前一个位置
        prev = self._history.pop()
        self._state.current_page = prev["page"]
        self._state.current_block_idx = prev["block_idx"]
        self._state.current_line_idx = prev["line_idx"]
        self._save_state()
        
        return {
            "page": self._state.current_page,
            "block_idx": self._state.current_block_idx,
            "line_idx": self._state.current_line_idx
        }
    
    def go_forward(self) -> Optional[Dict]:
        """前进"""
        if not self._redo_stack:
            return None
        
        # 保存当前位置到历史
        self._history.append({
            "page": self._state.current_page,
            "block_idx": self._state.current_block_idx,
            "line_idx": self._state.current_line_idx
        })
        
        # 恢复下一个位置
        next_pos = self._redo_stack.pop()
        self._state.current_page = next_pos["page"]
        self._state.current_block_idx = next_pos["block_idx"]
        self._state.current_line_idx = next_pos["line_idx"]
        self._save_state()
        
        return next_pos
    
    def get_progress(self) -> Dict:
        """获取阅读进度"""
        if self._state.total_blocks == 0:
            percentage = 0
        else:
            percentage = int((self._state.current_block_idx / self._state.total_blocks) * 100)
        
        return {
            "page": self._state.current_page,
            "total_pages": self._state.total_pages,
            "block_idx": self._state.current_block_idx,
            "total_blocks": self._state.total_blocks,
            "percentage": percentage
        }
    
    # === 书签操作 ===
    
    def add_bookmark(self, page: int, block_id: int, note: str = "") -> BookmarkData:
        """添加书签"""
        bookmark = BookmarkData(
            id=len(self._bookmarks) + 1,
            page=page,
            block_id=block_id,
            note=note,
            created_at=time.strftime("%Y-%m-%d %H:%M:%S")
        )
        self._bookmarks.append(bookmark)
        self._save_bookmarks()
        return bookmark
    
    def get_bookmarks(self) -> List[BookmarkData]:
        """获取所有书签"""
        return self._bookmarks
    
    def delete_bookmark(self, bookmark_id: int) -> bool:
        """删除书签"""
        for i, b in enumerate(self._bookmarks):
            if b.id == bookmark_id:
                self._bookmarks.pop(i)
                self._save_bookmarks()
                return True
        return False
    
    def clear(self):
        """清除所有状态"""
        self._state = ReadingState()
        self._history.clear()
        self._redo_stack.clear()
        self._save_state()
