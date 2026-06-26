# ChromaDB官方插件 - API使用示例
本插件100%兼容现有LanceDB调用接口，现有业务代码无需任何修改即可直接使用。

## 📋 通用API接口（和LanceDB完全一致）
### 1. 初始化向量库
```python
from core.vector_store import get_vector_store

# 自动读取配置文件，自动判断向量库类型
vs = get_vector_store()
```

### 2. 写入向量数据
```python
# 单条写入
vs.add(
    texts=["这是测试文本"],
    metadatas=[{"source": "test", "category": "文档"}],
    ids=["test_001"]
)

# 批量写入
vs.add(
    texts=["文本1", "文本2", "文本3"],
    metadatas=[
        {"source": "doc1", "category": "技术文档"},
        {"source": "doc2", "category": "行业动态"},
        {"source": "doc3", "category": "项目文档"}
    ],
    ids=["doc_001", "doc_002", "doc_003"]
)
```

### 3. 向量检索
```python
# 基础检索，返回top_k个结果
results = vs.query(
    query_texts=["如何优化向量检索准确率？"],
    n_results=5
)

# 带过滤条件的检索
results = vs.query(
    query_texts=["向量数据库性能优化"],
    n_results=10,
    where={"category": "技术文档"}  # 只返回分类为技术文档的结果
)

# 相似度过滤检索
results = vs.query(
    query_texts=["记忆进化成长项目架构"],
    n_results=5,
    min_score=0.6  # 只返回相似度大于0.6的结果
)
```

### 4. 删除数据
```python
# 按ID删除
vs.delete(ids=["test_001", "doc_002"])

# 按条件删除
vs.delete(where={"source": "test"})  # 删除所有来源为test的文档

# 清空整个集合
vs.delete_all()
```

### 5. 统计信息
```python
# 获取总文档数
count = vs.count()
print(f"总文档数：{count}")

# 获取所有ID列表
all_ids = vs.get_all_ids()

# 检查ID是否存在
exists = vs.exists("doc_001")
```

## ✨ ChromaDB专属扩展API
### 1. 集合管理
```python
# 创建新集合
vs.create_collection("collection_name", metadata={"description": "新集合"})

# 切换集合
vs.switch_collection("collection_name")

# 删除集合
vs.delete_collection("collection_name")

# 列出所有集合
collections = vs.list_collections()
```

### 2. 高级检索
```python
# 混合检索（关键词+向量）
results = vs.hybrid_query(
    query_texts=["混合检索技术"],
    n_results=10,
    keyword_weight=0.3,  # 关键词权重
    vector_weight=0.7   # 向量权重
)

# 多查询并行检索
results = vs.batch_query(
    query_texts=["问题1", "问题2", "问题3"],
    n_results=5
)
```

### 3. 数据导出导入
```python
# 导出整个集合到JSON文件
vs.export_to_json("backup.json")

# 从JSON文件导入数据
vs.import_from_json("backup.json", append=True)  # append=True不覆盖现有数据
```

## 📊 返回结果格式说明
所有检索返回结果格式统一：
```python
{
    "ids": [["doc_001", "doc_002", "doc_003"]],  # 文档ID列表
    "documents": [["文档1内容", "文档2内容", "文档3内容"]],  # 文档内容
    "metadatas": [[
        {"source": "doc1", "category": "技术文档"},
        {"source": "doc2", "category": "行业动态"},
        {"source": "doc3", "category": "项目文档"}
    ]],  # 元数据
    "distances": [[0.123, 0.234, 0.345]]  # 距离分数，越小相似度越高
}
```

## 🚀 代码迁移示例
### 原有LanceDB代码
```python
from core.vector_store import LanceDBStore

vs = LanceDBStore(
    path="I:/OpenClaw/知识库/lancedb",
    model="BAAI/bge-m3"
)

results = vs.query(
    query_texts=["测试查询"],
    n_results=5
)
```

### 切换到ChromaDB后代码无需修改
```python
from core.vector_store import get_vector_store

vs = get_vector_store()  # 自动根据配置初始化，无需修改参数

results = vs.query(
    query_texts=["测试查询"],
    n_results=5
)
```

---
**文档版本**: v1.0.0
**更新时间**: 2026-03-29 13:27
**作者**: 岚岚
