"""
L1 热存储 - 内存字典实现 (无需Redis)
"""
import time
from typing import Optional, Dict, Any
from app.models import MemoryItem, MemoryLevel


class L1HotStorage:
    """L1热存储 - 纯内存实现"""
    
    def __init__(self):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.max_size = 100 * 1024  # 100KB
        self.ttl = 3600  # 1小时
    
    async def init(self):
        """初始化 (无需操作)"""
        print("[L1] Memory cache initialized (no Redis)")
    
    async def get(self, key: str) -> Optional[MemoryItem]:
        """获取记忆"""
        item = self.cache.get(f"memory:{key}")
        if not item:
            return None
        
        # 检查TTL
        if time.time() - item.get("timestamp", 0) > self.ttl:
            del self.cache[f"memory:{key}"]
            return None
        
        import pickle
        try:
            item_dict = pickle.loads(item["data"])
            return MemoryItem(**item_dict)
        except Exception:
            return None
    
    async def set(self, key: str, item: MemoryItem) -> bool:
        """存储记忆"""
        import pickle
        try:
            data = pickle.dumps(item.model_dump())
            self.cache[f"memory:{key}"] = {
                "data": data,
                "timestamp": time.time()
            }
            return True
        except Exception as e:
            print(f"[L1] Set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """删除记忆"""
        if f"memory:{key}" in self.cache:
            del self.cache[f"memory:{key}"]
            return True
        return False
    
    async def exists(self, key: str) -> bool:
        """检查是否存在"""
        return f"memory:{key}" in self.cache
    
    async def keys(self, pattern: str = "*") -> list:
        """获取所有key"""
        return [k.replace("memory:", "") for k in self.cache.keys()]
    
    async def stats(self) -> dict:
        """获取统计信息"""
        size = sum(len(item["data"]) for item in self.cache.values())
        return {
            "entries": len(self.cache),
            "size_bytes": size,
            "size_mb": round(size / 1024 / 1024, 2)
        }
    
    async def close(self):
        """关闭 (无需操作)"""
        pass


# 单例
_l1_storage: Optional[L1HotStorage] = None


async def get_l1_storage() -> L1HotStorage:
    """获取L1存储单例"""
    global _l1_storage
    if _l1_storage is None:
        _l1_storage = L1HotStorage()
        await _l1_storage.init()
    return _l1_storage