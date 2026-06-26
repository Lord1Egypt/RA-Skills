"""缓存管理 - PDF Reader"""
import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from collections import OrderedDict

from .blocks import BlockData

logger = logging.getLogger(__name__)


class LRUCache:
    """LRU缓存"""
    
    def __init__(self, max_size: int = 100):
        self.max_size = max_size
        self._cache: OrderedDict = OrderedDict()
    
    def get(self, key: str) -> Optional[Any]:
        if key in self._cache:
            # 移到末尾（最近使用）
            self._cache.move_to_end(key)
            return self._cache[key]
        return None
    
    def set(self, key: str, value: Any):
        if key in self._cache:
            self._cache.move_to_end(key)
        else:
            if len(self._cache) >= self.max_size:
                # 删除最旧的
                self._cache.popitem(last=False)
        self._cache[key] = value
    
    def clear(self):
        self._cache.clear()
    
    def __contains__(self, key: str) -> bool:
        return key in self._cache


class PDFCache:
    """PDF缓存管理器"""
    
    def __init__(self, cache_dir: str = None):
        if cache_dir:
            self.cache_dir = Path(cache_dir)
        else:
            self.cache_dir = Path.home() / ".cache" / "deep-reading"
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self._page_cache = LRUCache(max_size=5)
        self._metadata_cache: Dict[str, Dict] = {}
    
    def get_cache_key(self, pdf_path: str) -> str:
        """生成缓存键（基于文件hash）"""
        path = Path(pdf_path)
        if path.exists():
            stat = path.stat()
            key = f"{path.name}_{stat.st_size}_{stat.st_mtime}"
            return hashlib.md5(key.encode()).hexdigest()
        return hashlib.md5(pdf_path.encode()).hexdigest()
    
    def get_pdf_dir(self, pdf_path: str) -> Path:
        """获取该 PDF 的专属目录（解析结果、进度、书签均保存在此）"""
        key = self.get_cache_key(pdf_path)
        pdf_dir = self.cache_dir / key
        pdf_dir.mkdir(parents=True, exist_ok=True)
        return pdf_dir
    
    def get_page(self, pdf_path: str, page_num: int) -> Optional[List[Dict]]:
        """获取缓存的页面"""
        cache_key = self.get_cache_key(pdf_path)
        full_key = f"{cache_key}_page_{page_num}"
        return self._page_cache.get(full_key)
    
    def set_page(self, pdf_path: str, page_num: int, data: List[Dict]):
        """缓存页面"""
        cache_key = self.get_cache_key(pdf_path)
        full_key = f"{cache_key}_page_{page_num}"
        self._page_cache.set(full_key, data)
    
    def get_metadata(self, pdf_path: str) -> Optional[Dict]:
        """获取缓存的元数据"""
        cache_key = self.get_cache_key(pdf_path)
        return self._metadata_cache.get(cache_key)
    
    def set_metadata(self, pdf_path: str, metadata: Dict):
        """缓存元数据"""
        cache_key = self.get_cache_key(pdf_path)
        self._metadata_cache[cache_key] = metadata
    
    def load_index(self, pdf_path: str) -> Optional[Dict]:
        """加载索引文件"""
        index_file = self.get_pdf_dir(pdf_path) / "index.json"
        if index_file.exists():
            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        return None
    
    def save_index(self, pdf_path: str, index_data: Dict):
        """保存索引文件"""
        index_file = self.get_pdf_dir(pdf_path) / "index.json"
        try:
            with open(index_file, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning("保存索引失败: %s", e)
    
    def has_cache(self, pdf_path: str) -> bool:
        """检查是否存在有效缓存（索引文件）"""
        index_path = self.cache_dir / self.get_cache_key(pdf_path) / "index.json"
        return index_path.exists()
    
    def load_page_from_disk(self, pdf_path: str, page_num: int) -> Optional[List[BlockData]]:
        """从磁盘加载指定页的块数据"""
        page_file = self.get_pdf_dir(pdf_path) / f"p{page_num}.json"
        if not page_file.exists():
            return None
        
        try:
            with open(page_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [BlockData.from_dict(b) for b in data]
        except Exception as e:
            logger.warning("加载页面缓存失败 %s: %s", page_file, e)
            return None
    
    def save_page_to_disk(self, pdf_path: str, page_num: int, blocks: List[BlockData]):
        """将指定页的块数据保存到磁盘"""
        page_file = self.get_pdf_dir(pdf_path) / f"p{page_num}.json"
        try:
            data = [b.to_dict() for b in blocks]
            with open(page_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=0)
        except Exception as e:
            logger.warning("保存页面缓存失败 %s: %s", page_file, e)
    
    def delete_page(self, pdf_path: str, page_num: int):
        """删除指定页的缓存"""
        pdf_dir = self.get_pdf_dir(pdf_path)
        page_file = pdf_dir / f"p{page_num}.json"
        if page_file.exists():
            try:
                page_file.unlink()
            except Exception as e:
                logger.warning("删除页面缓存失败 %s: %s", page_file, e)
    
    def clear(self):
        """清除所有缓存"""
        self._page_cache.clear()
        self._metadata_cache.clear()
    
    def get_cache_size(self) -> int:
        """获取缓存大小（MB估算）"""
        total = 0
        for value in self._page_cache._cache.values():
            total += len(str(value).encode('utf-8'))
        return total // (1024 * 1024)
