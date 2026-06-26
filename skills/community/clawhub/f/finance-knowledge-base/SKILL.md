---
name: Financial Industry Knowledge Base Manager
slug: finance-knowledge-base
description: AI-powered financial industry knowledge base manager — covers document organization, knowledge graph construction, semantic search, and intelligent Q&A. Built for financial institutions' internal knowledge management. Keywords: knowledge management, knowledge base, document management, semantic search, RAG, 知识库, 知识管理, 文档管理, 语义搜索, RAG, 知识图谱, 智能问答, 文档检索, 内部知识库, 企业知识管理.
version: 1.0.0

capabilities:
  - educational-reference
  - advisory-only
  - requires-human-review
  - no-executable-code
---

# Financial Industry Knowledge Base Manager / 金融行业知识库

> **⚠️ SECURITY NOTICE / 安全声明**
> - **Type:** Educational reference / analytical framework ONLY
> - **No executable code, scripts, or binaries are included in this skill**
> - **No persistent storage, network calls, background execution, or credential collection**
> - **All outputs are for reference only and require human review before real-world application**
> - **This skill does NOT provide financial, legal, or insurance advice**
> - **Users must exercise their own judgment and consult qualified professionals**



> **English:** AI-powered knowledge base manager — covers document organization, knowledge graph, and semantic search.
>
> **中文:** 知识库管理器——覆盖文档组织、知识图谱、语义搜索。

---

## Industry Pain Points / 行业痛点

| Pain Point / 痛点 | Impact / 影响 | Solution / 本Skill解决方案 |
|------------------|-------------|------------------------|
| **知识分散** | 文档散落各处，难找 | 统一知识库管理 |
| **知识孤岛** | 部门间知识不共享 | 跨部门知识共享 |
| **更新滞后** | 制度更新后知识未同步 | 知识版本管理 |
| **检索不准** | 关键词搜索效果差 | 语义搜索 |

---

## Trigger Keywords / 触发关键词

**English Triggers:** knowledge management, knowledge base, document management, semantic search, RAG

**中文触发词（优先）：** 知识库 / 知识管理 / 文档管理 / 语义搜索 / 知识图谱 / RAG / 检索 / 查询

---

## Core Capabilities / 核心能力

### 1. Document Organization / 文档组织

```python
KNOWLEDGE_STRUCTURE = {
    "regulations": {
        "banking": ["监管法规", "合规要求", "检查清单"],
        "insurance": ["监管法规", "产品规则", "偿付能力"],
        "securities": ["证监会规则", "交易所规则", "自律规则"]
    },
    "products": {
        "banking": ["存款产品", "贷款产品", "理财", "信用卡"],
        "insurance": ["寿险", "财险", "健康险", "团险"],
        "securities": ["股票", "债券", "基金", "期权"]
    },
    "processes": {
        "操作规程": [...],
        "风险控制": [...],
        "客户服务": [...]
    }
}
```

### 2. RAG Search / RAG检索

```python
class KnowledgeBaseSearch:
    """知识库语义搜索"""
    
    def semantic_search(self, query: str, top_k: int = 5) -> list:
        """语义搜索"""
        # 1. Query embedding
        query_vector = embed_text(query)
        
        # 2. 向量相似度搜索
        results = vector_search(query_vector, top_k)
        
        # 3. Reranking
        reranked = rerank(query, results)
        
        # 4. 生成答案
        context = "\n".join([r["content"] for r in reranked])
        answer = generate_answer(query, context)
        
        return {
            "answer": answer,
            "sources": reranked
        }
```

---

## Disclaimer

This skill provides knowledge management tools for educational purposes.
