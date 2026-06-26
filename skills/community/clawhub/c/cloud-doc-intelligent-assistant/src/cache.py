"""简单的文档缓存模块"""

import hashlib
import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional


class DocumentCache:
    """文档缓存类，用于缓存抓取的文档内容"""
    
    def __init__(self, cache_dir: str = "./cache", ttl_hours: int = 24):
        """
        Args:
            cache_dir: 缓存目录
            ttl_hours: 缓存有效期（小时）
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_cache_key(self, cloud: str, doc_ref: str) -> str:
        """生成缓存键"""
        key_str = f"{cloud}:{doc_ref}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """获取缓存文件路径"""
        return self.cache_dir / f"{cache_key}.json"
    
    def get(self, cloud: str, doc_ref: str) -> Optional[dict]:
        """获取缓存的文档"""
        cache_key = self._get_cache_key(cloud, doc_ref)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)
            
            # 检查缓存是否过期
            cached_time = datetime.fromisoformat(cached_data.get('cached_at', ''))
            if datetime.now() - cached_time > self.ttl:
                logging.debug(f"缓存已过期: {doc_ref}")
                cache_path.unlink()  # 删除过期缓存
                return None
            
            logging.info(f"使用缓存: {doc_ref}")
            return cached_data.get('data')
        
        except Exception as e:
            logging.warning(f"读取缓存失败: {e}")
            return None
    
    def set(self, cloud: str, doc_ref: str, data: dict) -> None:
        """设置缓存"""
        cache_key = self._get_cache_key(cloud, doc_ref)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            cached_data = {
                'cached_at': datetime.now().isoformat(),
                'cloud': cloud,
                'doc_ref': doc_ref,
                'data': data
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cached_data, f, ensure_ascii=False, indent=2)
            
            logging.debug(f"已缓存: {doc_ref}")
        
        except Exception as e:
            logging.warning(f"写入缓存失败: {e}")
    
    def clear_expired(self) -> int:
        """清理过期缓存，返回清理的文件数量"""
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                
                cached_time = datetime.fromisoformat(cached_data.get('cached_at', ''))
                if datetime.now() - cached_time > self.ttl:
                    cache_file.unlink()
                    count += 1
            
            except Exception as e:
                logging.warning(f"清理缓存失败 {cache_file}: {e}")
        
        if count > 0:
            logging.info(f"已清理 {count} 个过期缓存文件")
        
        return count
