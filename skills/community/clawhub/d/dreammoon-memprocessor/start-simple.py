#!/usr/bin/env python3
"""
简化启动脚本 - 跳过FAISS和SentenceTransformer
支持完整的L1/L2/L3存储和关键词搜索
使用端口9090
"""
import sys
sys.path.insert(0, '/root/DreamMoon/config/dreammoon-memory-python')

# 模拟FAISS模块
class MockIndex:
    """模拟FAISS索引"""
    def __init__(self, dim=384):
        self.dim = dim
        self._data = []
    
    def add(self, vec):
        self._data.append(vec)
    
    def search(self, query, k=5):
        return [[0.0]*k], [[-1]*k]
    
    @property
    def ntotal(self):
        return len(self._data)

class MockFaiss:
    """模拟FAISS模块"""
    IndexFlatIP = MockIndex
    
    @staticmethod
    def read_index(path):
        return MockIndex()
    
    @staticmethod
    def write_index(index, path):
        pass
    
    @staticmethod
    def normalize_L2(vectors):
        pass

# 模拟SentenceTransformer
class MockSentenceTransformer:
    """模拟SentenceTransformer"""
    def __init__(self, model_name=None):
        self.model_name = model_name or "mock-model"
    
    def encode(self, texts, **kwargs):
        import numpy as np
        if isinstance(texts, str):
            texts = [texts]
        # 返回随机向量作为模拟
        return np.random.randn(len(texts), 384).astype(np.float32)
    
    @property
    def get_sentence_embedding_dimension(self):
        return 384

# 模拟sentence_transformers模块
class MockSentenceTransformers:
    SentenceTransformer = MockSentenceTransformer

# 替换模块
sys.modules['faiss'] = MockFaiss()
sys.modules['sentence_transformers'] = MockSentenceTransformers()
sys.modules['sentence_transformers.SentenceTransformer'] = MockSentenceTransformer

# 导入并启动
print("🚀 启动 DreamMoon-MemoryProcessor (简化版)")
print("   注意: 向量检索功能使用模拟，其他功能正常")
print("   端口: 9090")
print()

try:
    from app.main import app
    import uvicorn
    
    print("📡 服务启动中...")
    print("   地址: http://0.0.0.0:9090")
    print("   文档: http://localhost:9090/docs")
    print()
    
    uvicorn.run(app, host="0.0.0.0", port=9090, reload=False)
    
except Exception as e:
    print(f"❌ 启动失败: {e}")
    import traceback
    traceback.print_exc()
