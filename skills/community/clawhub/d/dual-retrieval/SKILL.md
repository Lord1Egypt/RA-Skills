# Dual Retrieval Skill - Phase 4

## 描述
双重检索：M-Flow（图拓扑检索）+ QMD（BM25+向量检索）优势互补。

## M-Flow vs QMD 对比

| 特性 | M-Flow | QMD |
|------|--------|-----|
| 检索方式 | 图拓扑 + Bundle Search | BM25 + 向量 + rerank |
| 适合场景 | 精确问答、多跳推理 | 关键词搜索、语义相似 |
| 记忆结构 | 四层 Cone Graph | 多 Collection |
| 优势 | 时间推理、关联推理 | 灵活、已配置 |

## 工作流程

```
Query → 
  ├── M-Flow.search() → Episode + Facet + Entity
  └── QMD search → 文件 + 片段
      ↓
结果合并 → 去重 → 排序 → 返回
```

## 文件结构

```
dual-retrieval/
├── SKILL.md
├── scripts/
│   ├── __init__.py      # DualRetrievalPipeline
│   └── test_dual.py     # 测试
```

## 依赖
- m-flow-memory skill (MFlowMemory)
- QMD (qmd tools)
