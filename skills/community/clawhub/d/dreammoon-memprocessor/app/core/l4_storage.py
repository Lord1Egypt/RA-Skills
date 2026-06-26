"""L4 归档存储 - FAISS向量索引 + 文件压缩"""
import json
import pickle
import tarfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import faiss
import numpy as np

from app.config import settings
from app.models import MemoryItem, MemoryLevel, SearchResult


class L4ArchiveStorage:
    """L4归档存储 - FAISS向量索引"""
    
    def __init__(self):
        self.archive_dir = settings.L4_ARCHIVE_DIR
        self.vector_index_path = settings.L4_VECTOR_INDEX_PATH
        self.metadata_path = settings.L4_METADATA_PATH
        
        self.index: Optional[faiss.Index] = None
        self.metadata: List[Dict] = []
        self.dimension = settings.EMBEDDING_DIMENSION
        
        self._initialized = False
    
    async def init(self):
        """初始化向量索引"""
        if self._initialized:
            return
        
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        settings.L4_VECTOR_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        
        # 加载或创建索引
        if self.vector_index_path.exists():
            self.index = faiss.read_index(str(self.vector_index_path))
            print(f"[L4] Loaded existing index with {self.index.ntotal} vectors")
        else:
            # 创建新的内积索引（归一化后等同于余弦相似度）
            self.index = faiss.IndexFlatIP(self.dimension)
            print(f"[L4] Created new vector index")
        
        # 加载元数据
        if self.metadata_path.exists():
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        
        self._initialized = True
        print(f"[L4] Archive storage initialized")
    
    async def add(self, item: MemoryItem, embedding: List[float]):
        """添加向量和元数据"""
        await self.init()
        
        if not embedding or len(embedding) != self.dimension:
            raise ValueError(f"Invalid embedding dimension: {len(embedding) if embedding else 0}")
        
        # 归一化向量
        vec = np.array([embedding], dtype='float32')
        faiss.normalize_L2(vec)
        
        # 添加到索引
        self.index.add(vec)
        
        # 保存元数据
        meta = {
            "id": item.id,
            "key": item.key,
            "content": item.content[:500],  # 限制长度
            "level": item.level.value,
            "created_at": item.created_at.isoformat(),
            "tags": item.tags
        }
        self.metadata.append(meta)
        
        # 持久化
        await self._save()
        
        print(f"[L4] Added vector for: {item.key}")
    
    async def search(self, query_embedding: List[float], top_k: int = 5) -> List[SearchResult]:
        """向量相似度搜索"""
        await self.init()
        
        if self.index.ntotal == 0:
            return []
        
        # 归一化查询向量
        query_vec = np.array([query_embedding], dtype='float32')
        faiss.normalize_L2(query_vec)
        
        # 搜索
        scores, indices = self.index.search(query_vec, min(top_k, self.index.ntotal))
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < 0 or idx >= len(self.metadata):
                continue
            
            meta = self.metadata[idx]
            results.append(SearchResult(
                id=meta["id"],
                key=meta["key"],
                content=meta["content"],
                similarity=float(score),  # 归一化后的内积 = 余弦相似度
                level=MemoryLevel(meta.get("level", "l4_archive")),
                metadata=meta,
                created_at=datetime.fromisoformat(meta["created_at"])
            ))
        
        return results
    
    async def archive_old_memories(self, days: int = 90):
        """归档旧的L3记忆"""
        await self.init()
        
        from app.core.l3_storage import get_l3_storage
        l3 = await get_l3_storage()
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # 获取所有每日摘要文件
        files = list(l3.daily_dir.glob("*.md"))
        to_archive = []
        
        for file_path in files:
            # 从文件名解析日期
            try:
                file_date = datetime.strptime(file_path.stem, "%Y-%m-%d")
                if file_date < cutoff_date:
                    to_archive.append(file_path)
            except ValueError:
                continue
        
        if not to_archive:
            print(f"[L4] No old memories to archive")
            return
        
        # 按月分组
        by_month: Dict[str, List[Path]] = {}
        for file_path in to_archive:
            month = file_path.stem[:7]  # YYYY-MM
            if month not in by_month:
                by_month[month] = []
            by_month[month].append(file_path)
        
        # 创建压缩包
        for month, files in by_month.items():
            await self._create_monthly_archive(month, files, l3)
        
        print(f"[L4] Archived {len(to_archive)} files")
    
    async def _create_monthly_archive(self, month: str, files: List[Path], l3):
        """创建月度归档"""
        archive_path = self.archive_dir / "memory" / f"{month}.tar.gz"
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 创建tar.gz
        with tarfile.open(archive_path, "w:gz") as tar:
            for file_path in files:
                tar.add(file_path, arcname=file_path.name)
        
        # 删除原始文件
        for file_path in files:
            file_path.unlink()
        
        print(f"[L4] Created archive: {archive_path}")
    
    async def get_stats(self) -> Dict:
        """统计信息"""
        await self.init()
        
        return {
            "total_vectors": self.index.ntotal if self.index else 0,
            "metadata_entries": len(self.metadata),
            "dimension": self.dimension
        }
    
    async def _save(self):
        """保存索引和元数据"""
        if self.index:
            faiss.write_index(self.index, str(self.vector_index_path))
        
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
    
    async def close(self):
        """关闭并保存"""
        await self._save()


# 单例
_l4_storage: Optional[L4ArchiveStorage] = None


async def get_l4_storage() -> L4ArchiveStorage:
    """获取L4存储单例"""
    global _l4_storage
    if _l4_storage is None:
        _l4_storage = L4ArchiveStorage()
        await _l4_storage.init()
    return _l4_storage
