---
name: bm25-rerank-memory
description: 本地 BM25 + Embedding + Rerank 混合记忆检索。检索 /root/workspace/Remember 下的 Markdown 记忆文件，支持关键词+语义+重排。每次记忆搜索用它替代 mem0。
---

# BM25 Rerank Memory Search

调用本地检索脚本 `/opt/memory/bm25_rerank_search.py`，返回精确的上下文片段。

## 依赖
- BM25: `rank_bm25`
- 向量+重排: SiliconFlow API (BAAI/bge-m3 + BAAI/bge-reranker-v2-m3)
- 安装: `pip install rank-bm25 --break-system-packages`

## 使用方式

### 搜索记忆
```bash
python3 /opt/memory/bm25_rerank_search.py search <查询词>
```

### 重建索引（记忆文件变更后需执行）
```bash
python3 /opt/memory/bm25_rerank_search.py reindex
```

## 检索逻辑
1. BM25 关键词匹配 → 候选集 A
2. BGE-M3 向量相似度 → 候选集 B
3. A ∪ B 合并
4. BGE-Reranker-v2-m3 重排 → 最终结果

## 输出格式
每条结果包含: `[score] path:chunk_id` + 内容片段 (最多显示前200字符)
