#!/usr/bin/env python3
"""
向量存储 V1 - ChromaDB 语义检索
用于替代纯文件检索，提升搜索准确率
"""
import json, hashlib
from pathlib import Path
from typing import Dict, List, Optional
import chromadb
from chromadb.config import Settings

class VectorStore:
    def __init__(self, memory_dir: Path):
        self.memory_dir = memory_dir
        self.persist_dir = str(memory_dir / '.chroma')
        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="memory_vectors",
            metadata={"hnsw:space": "cosine"}
        )

    def add_memory(self, text: str, metadata: Dict = None) -> str:
        """添加一条向量记忆"""
        mid = hashlib.md5(text.encode()).hexdigest()[:16]
        
        # 检查是否已存在
        existing = self.collection.get(ids=[mid])
        if existing and existing['ids']:
            # 更新计数
            return mid

        metadata = metadata or {}
        self.collection.add(
            documents=[text],
            metadatas=[{
                'date': metadata.get('date', ''),
                'category': metadata.get('category', 'general'),
                'importance': metadata.get('importance', 5),
                'tier': metadata.get('tier', 'short_term'),
                'source': metadata.get('source', ''),
            }],
            ids=[mid]
        )
        return mid

    def search(self, query: str, n: int = 5, filter_dict: Dict = None) -> List[Dict]:
        """语义搜索记忆"""
        where = filter_dict or None
        results = self.collection.query(
            query_texts=[query],
            n_results=n,
            where=where
        )
        
        if not results or not results['ids']:
            return []
        
        items = []
        for i in range(len(results['ids'][0])):
            items.append({
                'id': results['ids'][0][i],
                'text': results['documents'][0][i] if results['documents'] else '',
                'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                'distance': results['distances'][0][i] if results.get('distances') else 0,
            })
        return items

    def search_by_category(self, query: str, category: str, n: int = 5) -> List[Dict]:
        """按分类语义搜索"""
        return self.search(query, n, {"category": category})

    def search_by_tier(self, query: str, tier: str, n: int = 5) -> List[Dict]:
        """按层级语义搜索"""
        return self.search(query, n, {"tier": tier})

    def search_core(self, query: str, n: int = 5) -> List[Dict]:
        """搜索核心记忆"""
        return self.search(query, n, {"tier": "core"})

    def sync_from_memory_file(self):
        """从memory目录同步到向量库"""
        count = 0
        for f in sorted(self.memory_dir.glob('*.md')):
            content = f.read_text(encoding='utf-8', errors='ignore')
            lines = [l for l in content.split('\n') if l.strip() and not l.startswith('#') and not l.startswith('>')]
            for line in lines:
                if len(line) > 20:  # 忽略太短的行
                    self.add_memory(line.strip()[:500], {
                        'date': f.stem,
                        'category': 'general',
                        'source': f.name,
                    })
                    count += 1
        self.collection = self.client.get_collection("memory_vectors")
        return count

    def get_stats(self) -> Dict:
        count = self.collection.count()
        return {
            'total_vectors': count,
            'chroma_version': chromadb.__version__,
        }

if __name__ == '__main__':
    vs = VectorStore(Path.home() / '.agent-mem/memory')
    print(f"📊 向量库: {vs.get_stats()}")
    print("同步记忆文件...")
    c = vs.sync_from_memory_file()
    print(f"   同步了 {c} 条向量")
    print(f"   总向量: {vs.collection.count()}")

    print("\n搜索测试: '记忆引擎'")
    for r in vs.search("记忆引擎", n=3):
        print(f"  [{r['distance']:.3f}] {r['text'][:60]}...")
