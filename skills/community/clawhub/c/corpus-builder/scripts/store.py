#!/usr/bin/env python3
"""
Vector Store - 向量存储

使用 ChromaDB 进行向量存储和语义搜索。
"""

# 在导入 chromadb 之前设置 sqlite3
import sys
from pathlib import Path

# 优先使用 pysqlite3-binary (需要 sqlite3 >= 3.35.0)
try:
    import pysqlite3 as sqlite3

    sys.modules["sqlite3"] = sqlite3
except ImportError:
    pass

# 支持两种导入方式：作为模块导入 or 直接运行
try:
    from .chunker import Chunk
except ImportError:
    # 如果相对导入失败，尝试绝对导入
    parent_dir = Path(__file__).resolve().parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    from chunker import Chunk

from typing import Dict, List

import chromadb


class VectorStore:
    """向量存储 - ChromaDB 集成"""

    def __init__(self, persist_directory: str = "./corpus/chroma"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.persist_directory = persist_directory

    def create_collection(
        self, name: str, metadata: Dict = None
    ) -> chromadb.Collection:
        """创建语料集合"""
        metadata = metadata or {}
        metadata.update(
            {
                "hnsw:space": "cosine",
                "hnsw:construction_ef": 128,
                "hnsw:search_ef": 64,
            }
        )

        return self.client.get_or_create_collection(name=name, metadata=metadata)

    def _flatten_metadata(self, annotation: Dict) -> Dict:
        """将嵌套的标注字典扁平化，适配 ChromaDB"""
        metadata = {}

        # 列表类型转为逗号分隔字符串
        list_fields = ["scene_type", "emotion", "techniques", "key_elements", "usage"]
        for fld in list_fields:
            if fld in annotation:
                metadata[fld] = ",".join(annotation[fld])

        # 标量类型直接复制
        scalar_fields = [
            "pace",
            "pov",
            "character_count",
            "power_level",
            "quality_score",
            "text_length",
            "annotation_model",
        ]
        for fld in scalar_fields:
            if fld in annotation:
                metadata[fld] = str(annotation[fld])

        # 源文件信息
        if "source_file" in annotation:
            metadata["source_file"] = annotation["source_file"]

        return metadata

    def add_annotated_chunks(
        self, collection: chromadb.Collection, chunks: List[Chunk]
    ):
        """添加标注后的语料到向量库"""
        ids = []
        documents = []
        metadatas = []

        for i, chunk in enumerate(chunks):
            chunk_id = f"chunk_{i:06d}"
            ids.append(chunk_id)
            documents.append(chunk.text)

            # 添加标注数据到 metadata
            metadata = self._flatten_metadata(chunk.annotation)
            metadata["source_file"] = chunk.source_file
            metadata["chunk_type"] = chunk.chunk_type
            metadata["start"] = chunk.start
            metadata["end"] = chunk.end
            metadatas.append(metadata)

            # 批量提交（每 100 条）
            if len(ids) >= 100:
                collection.add(ids=ids, documents=documents, metadatas=metadatas)
                ids, documents, metadatas = [], [], []

        # 提交剩余
        if ids:
            collection.add(ids=ids, documents=documents, metadatas=metadatas)

    def search(
        self,
        collection: chromadb.Collection,
        query: str,
        filters: Dict = None,
        limit: int = 10,
    ) -> Dict:
        """
        语义搜索 + 元数据过滤

        参数:
        - collection: ChromaDB 集合
        - query: 搜索查询
        - filters: 过滤条件
        - limit: 返回数量

        返回:
        - results: 搜索结果
        """
        # 构建 where 条件
        where = None
        if filters:
            where = {}
            for key, value in filters.items():
                if isinstance(value, list):
                    where[key] = {"$contains": value[0]}
                elif isinstance(value, str) and ">=" in value:
                    field, val = value.split(">=")
                    where[field] = {"$gte": int(val)}
                elif isinstance(value, str) and "<=" in value:
                    field, val = value.split("<=")
                    where[field] = {"$lte": int(val)}
                else:
                    where[key] = value

        results = collection.query(
            query_texts=[query],
            n_results=limit,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        return results
