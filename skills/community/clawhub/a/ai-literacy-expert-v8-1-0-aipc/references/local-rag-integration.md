> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 本地 RAG 集成指南（V6）

## 概述
本指南说明如何将 OpenVINO 优化的 RAG（检索增强生成）能力集成到 AI 通识课教学系统中，实现教案知识库、课件检索、智能问答、团队知识管理等教学生产力场景。

## 技术选型

### 推荐模型与组件
| 组件 | 模型/工具 | OpenVINO 优化 | 用途 |
|------|----------|--------------|------|
| Embedding | BGE-small-zh-v1.5 | INT8 量化 | 中文文本向量化 |
| Embedding | BGE-m3 | FP16 | 多语言向量化 |
| 向量数据库 | ChromaDB | - | 本地向量存储与检索 |
| Reranker | BGE-reranker-v2-m3 | FP16 | 检索结果重排序 |
| 文档解析 | Unstructured / PyMuPDF | - | PDF/Word/PPT 解析 |

### 硬件加速策略
- **GPU/NPU**：Embedding 模型推理（向量化查询）
- **GPU**：Reranker 模型推理
- **CPU**：文档解析、分块、索引构建

## 部署架构

### Client/Server 模式
```python
# rag_service.py — 本地 RAG 微服务
from fastapi import FastAPI
from openvino.runtime import Core
import chromadb
from chromadb.utils import embedding_functions

app = FastAPI(title="AI通识课 RAG 服务", version="6.0.0")

# OpenVINO Embedding 模型
ie = Core()
embed_model = ie.compile_model(
    model="models/bge-small-zh-int8.xml",
    device_name="GPU.NPU"
)

# ChromaDB 向量数据库
chroma_client = chromadb.PersistentClient(path="./teaching_knowledge_base")

# 教学知识库集合
lesson_collection = chroma_client.get_or_create_collection(
    name="teaching_materials",
    embedding_function=OpenVINOEmbedding(embed_model)
)

@app.post("/api/v1/rag/ingest")
async def ingest_document(file_path: str, metadata: dict = None):
    """文档入库 — 将教案/课件/资料加入知识库"""
    # 1. 文档解析
    chunks = parse_document(file_path)  # PDF/Word/PPT → 文本块
    # 2. 文本分块
    chunks = chunk_text(chunks, chunk_size=512, overlap=64)
    # 3. 向量化并存储
    embeddings = embed_texts(chunks, embed_model)
    lesson_collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=[metadata or {}] * len(chunks),
        ids=[f"doc_{i}" for i in range(len(chunks))]
    )
    return {"status": "success", "chunks_added": len(chunks)}

@app.post("/api/v1/rag/query")
async def query_knowledge(query: str, top_k: int = 5, rerank: bool = True):
    """知识检索 — 从教案知识库中检索相关内容"""
    # 1. 查询向量化
    query_embedding = embed_text(query, embed_model)
    # 2. 向量检索
    results = lesson_collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k * 3 if rerank else top_k
    )
    # 3. 重排序（可选）
    if rerank:
        results = rerank_results(query, results)
    return {
        "status": "success",
        "data": {
            "answers": results["documents"][:top_k],
            "scores": results["distances"][:top_k],
            "metadata": results["metadatas"][:top_k]
        },
        "ai_tool": "rag",
        "hardware": {"gpu": True, "npu": True}
    }

@app.post("/api/v1/rag/chat")
async def knowledge_chat(question: str, context: str = None):
    """知识问答 — 基于知识库的智能问答"""
    # 1. 检索相关上下文
    retrieved = await query_knowledge(question)
    # 2. 构建 prompt
    context = "\n".join(retrieved["data"]["answers"])
    prompt = f"""基于以下教学资料回答问题：

资料：
{context}

问题：{question}

回答："""
    return {"status": "success", "prompt": prompt, "context": context}
```

### 启动服务
```bash
uvicorn rag_service:app --host 127.0.0.1 --port 8904
```

## 教学知识库构建

### 知识库结构
```
teaching_knowledge_base/
├── module_a/          # 模块A：认知基础
│   ├── a1_history.md  # AI 进化历程
│   ├── a2_concepts.md # AI 是什么
│   └── a3_collab.md   # 协作哲学
├── module_b/          # 模块B：工具操作
├── module_c/          # 模块C：方法论
├── module_d/          # 模块D：通用实练
├── module_e/          # 模块E：专业应用
├── module_f/          # 模块F：安全伦理
├── module_g/          # 模块G：最新发展
├── lesson_plans/      # 教案库
├── question_bank/     # 题库
└── teaching_cases/    # 教学案例
```

### 文档入库流程
```python
# 批量导入教案
async def bulk_ingest_teaching_materials(directory: str):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.pdf', '.docx', '.pptx')):
                file_path = os.path.join(root, file)
                metadata = {
                    "module": os.path.basename(root),
                    "source": file,
                    "type": file.split('.')[-1],
                    "ingest_time": datetime.now().isoformat()
                }
                await ingest_document(file_path, metadata)
```

## 教学场景集成

### 场景一：备课知识增强（能力三增强）
```javascript
// 备课时自动检索相关教案和素材
async function enhanceLessonPrep(topic, module) {
    const response = await fetch('http://127.0.0.1:8904/api/v1/rag/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: `${module} ${topic} 教案 教学设计`,
            top_k: 10,
            rerank: true
        })
    });
    const result = await response.json();
    return result.data.answers;  // 相关教案片段
}
```

### 场景二：团队知识管理（能力六增强）
```javascript
// 团队协作备课时检索共享知识库
async function searchTeamKnowledge(query, team_id) {
    const response = await fetch('http://127.0.0.1:8904/api/v1/rag/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            query: query,
            top_k: 5,
            filter: { team_id: team_id }
        })
    });
    return (await response.json()).data.answers;
}
```

## OpenVINO 优化步骤

### 1. Embedding 模型转换
```bash
# BGE-small-zh → OpenVINO IR + INT8 量化
optimum-cli export openvino --model BAAI/bge-small-zh-v1.5 --weight-format int8 models/bge-small-zh-int8
```

### 2. 性能验证
| 指标 | 目标值 | 测试方法 |
|------|--------|---------|
| 向量化速度 | >1000 句/秒 (GPU) | 10000 句测试集 |
| 检索延迟 | <50ms (top-5) | 10000 条知识库 |
| 召回率 | ≥85% | 教学问答测试集 |
| 准确率@3 | ≥75% | 教学问答测试集 |

## 错误降级
| 场景 | 降级方案 |
|------|---------|
| GPU/NPU 不可用 | 降级为 CPU 向量化 |
| RAG 服务崩溃 | 降级为内置知识库（硬编码） |
| 向量数据库损坏 | 从备份重建索引 |
| 检索结果质量差 | 增加 top_k 或切换 reranker |

## 质量门控
- [ ] 知识召回率 ≥85%
- [ ] 检索延迟 <50ms（top-5）
- [ ] 支持 PDF/Word/PPT/Markdown 格式入库
- [ ] 知识库容量 ≥10000 条文档
- [ ] 向量化速度 >1000 句/秒
- [ ] 数据完全本地存储，零云端传输
