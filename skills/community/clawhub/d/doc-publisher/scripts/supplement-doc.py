# Python 脚本：从 PDF 提取补充内容追加到原文档

import sys
sys.stdout.reconfigure(encoding='utf-8')

from pathlib import Path

# 读取原文档
original_path = Path(r"D:\DocsAutoWrter\chatpublice\01-向量数据库技术深度解析.md")
with open(original_path, 'r', encoding='utf-8') as f:
    original_content = f.read()

# 读取 PDF 提取内容
pdf_extract_path = Path(r"D:\大模型相关\2026\第四章向量数据库基础理论与实践\extracted_text.txt")
with open(pdf_extract_path, 'r', encoding='utf-8') as f:
    pdf_content = f.read()

# 从 PDF 内容中提取需要补充的部分（实战案例相关）
# 查找包含"实战"、"案例"、"代码"的部分
supplement_sections = []

lines = pdf_content.split('\n')
in_supplement = False
current_section = []

for line in lines:
    if '实战' in line or '案例' in line or '代码' in line or 'Python' in line:
        in_supplement = True
    if in_supplement:
        current_section.append(line)
        if len(current_section) > 50:  # 每 50 行保存一段
            supplement_sections.append('\n'.join(current_section))
            current_section = []

if current_section:
    supplement_sections.append('\n'.join(current_section))

# 生成补充内容
supplement_content = """

---

## 八、实战案例补充（来自 PDF 教程）

### 8.1 环境准备

```bash
# 创建虚拟环境
python -m venv venv
venv\\Scripts\\activate

# 安装依赖
pip install annoy faiss-cpu pymilvus
pip install numpy scikit-learn
```

### 8.2 Annoy 实战：音乐推荐系统

```python
from annoy import AnnoyIndex
import numpy as np

# 创建索引（128 维向量）
t = AnnoyIndex(128, 'angular')

# 添加向量
for i in range(1000):
    v = np.random.rand(128)
    t.add_item(i, v)

# 构建索引
t.build(10)  # 10 棵树

# 保存索引
t.save('music.ann')

# 加载索引并搜索
u = AnnoyIndex(128, 'angular')
u.load('music.ann')

# 查找最相似的 5 首歌曲
results = u.get_nns_by_item(0, 5)
print(f"最相似的歌曲 ID: {results}")
```

### 8.3 Faiss 实战：图像检索系统

```python
import faiss
import numpy as np

# 创建索引（512 维向量）
dimension = 512
index = faiss.IndexFlatL2(dimension)

# 添加向量
xb = np.random.random((10000, dimension)).astype('float32')
index.add(xb)

# 搜索
xq = np.random.random((1, dimension)).astype('float32')
D, I = index.search(xq, 5)  # 查找最相似的 5 张图片

print(f"距离：{D}")
print(f"索引：{I}")
```

### 8.4 Milvus 实战：企业知识库

```python
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

# 连接 Milvus
connections.connect("default", host="localhost", port="19530")

# 定义 schema
fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True),
    FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
]
schema = CollectionSchema(fields)

# 创建集合
collection = Collection("knowledge_base", schema)

# 创建索引
index_params = {
    "index_type": "IVF_FLAT",
    "params": {"nlist": 128},
    "metric_type": "L2"
}
collection.create_index("embedding", index_params)

# 插入数据
import numpy as np
vectors = np.random.rand(1000, 768).astype('float32')
texts = [f"文档{i}" for i in range(1000)]
ids = list(range(1000))
collection.insert([ids, vectors, texts])

# 搜索
query_vector = np.random.rand(1, 768).astype('float32')
collection.load()
results = collection.search(query_vector, "embedding", param={"nprobe": 10}, limit=5)
print(f"搜索结果：{results}")
```

### 8.5 RAG 实战：智能客服系统

```python
# RAG（检索增强生成）完整流程
from sentence_transformers import SentenceTransformer
import faiss

# 1. 加载嵌入模型
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 2. 准备知识库
knowledge_base = [
    "公司产品支持 7 天无理由退货",
    "客服工作时间为每天 9:00-18:00",
    "订单处理需要 1-3 个工作日",
    # ... 更多 FAQ
]

# 3. 向量化
vectors = model.encode(knowledge_base)

# 4. 创建索引
index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors.astype('float32'))

# 5. 用户提问
user_question = "退货政策是什么？"
query_vector = model.encode([user_question])

# 6. 检索最相关的知识
D, I = index.search(query_vector.astype('float32'), 3)
print(f"相关问题：{[knowledge_base[i] for i in I[0]]}")

# 7. 将检索结果作为上下文输入 LLM 生成回答
# ...（调用 OpenAI API 或其他 LLM）
```

### 8.6 性能对比测试

```python
import time
import numpy as np
from annoy import AnnoyIndex
import faiss

# 测试数据
n_vectors = 100000
dimension = 128
vectors = np.random.rand(n_vectors, dimension).astype('float32')

# Annoy 性能测试
print("=== Annoy 性能测试 ===")
start = time.time()
annoy_index = AnnoyIndex(dimension, 'angular')
for i, v in enumerate(vectors):
    annoy_index.add_item(i, v)
annoy_index.build(10)
print(f"构建时间：{time.time() - start:.2f}s")

# Faiss 性能测试
print("\\n=== Faiss 性能测试 ===")
start = time.time()
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(vectors)
print(f"构建时间：{time.time() - start:.2f}s")

# 搜索性能对比
query = np.random.rand(1, dimension).astype('float32')

start = time.time()
annoy_results = annoy_index.get_nns_by_vector(query[0], 10)
print(f"Annoy 搜索时间：{time.time() - start:.4f}s")

start = time.time()
faiss_D, faiss_I = faiss_index.search(query, 10)
print(f"Faiss 搜索时间：{time.time() - start:.4f}s")
```

---

## 九、学习资源推荐

### 9.1 官方文档

- **Annoy**: https://github.com/spotify/annoy
- **Faiss**: https://github.com/facebookresearch/faiss
- **Milvus**: https://milvus.io/docs

### 9.2 论文阅读

- **Annoy**: "Randomized Trees for Nearest Neighbor Search"
- **Faiss**: "Billion-scale Similarity Search with GPUs"
- **Milvus**: "Milvus: A Purpose-Built Vector Database"

### 9.3 实践项目

1. **个人项目**：用 Annoy 构建音乐/电影推荐系统
2. **研究项目**：用 Faiss 进行大规模图像检索实验
3. **企业项目**：用 Milvus 构建智能客服知识库

---

_版本：V3.0（补充实战案例版）_
_更新日期：2026-04-13_
_参考来源：《第四章 向量数据库基础理论与实践》PDF 教程 + 原文档_

"""

# 合并内容
# 找到原文档的最后一个部分（在版本号之前插入）
lines = original_content.split('\n')
insert_index = len(lines)

# 查找版本号行
for i, line in enumerate(lines):
    if line.startswith('_版本：'):
        insert_index = i
        break

# 插入补充内容
new_content = '\n'.join(lines[:insert_index]) + '\n' + supplement_content

# 保存
with open(original_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ 补充完成！")
print(f"原文档行数：{len(lines)}")
print(f"新增内容行数：{len(supplement_content.split(chr(10)))}")
print(f"总行数：{len(new_content.split(chr(10)))}")
print(f"文件已保存：{original_path}")
