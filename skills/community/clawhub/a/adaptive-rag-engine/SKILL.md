---
name: adaptive-rag-engine
version: 1.0.0
description: "Adaptive RAG 引擎 — 从线性检索到自主认知循环。集成胶囊预筛选、智能路由、CRAG纠错、L3校验。当需要搜索记忆/检索信息/回答复杂问题时触发。关键词：RAG、检索、记忆搜索、向量检索、Agentic RAG、CRAG。"
metadata:
  requires:
    bins: ["python3"]
---

# 🧠 Adaptive RAG Engine v1.0

> **不是管道，是认知循环。**

## 核心能力

| 能力 | 说明 | 触发方式 |
|------|------|---------|
| **Adaptive Router** | 判断是否需要检索，简单问题直接答 | 自动（每次 memory_search 前） |
| **Capsule Pre-filter** | 42个胶囊标题预匹配，缩小范围 90% | 自动（Router 通过后） |
| **Vector Search** | bge-m3 向量检索 Top-20 | memory_search 工具 |
| **LLM Re-rank** | 语义重排序 Top-20 → Top-5 | 检索后自动 |
| **CRAG Evaluator** | 质量评估 + 低分补搜 | 检索后自动 |
| **L3 Gatekeeper** | 输出前与核心洞察校验 | 生成前自动 |
| **Memory Bridge** | Active Memory ↔ Phoenix 双向桥接 | 对话结束时 |

## 使用流程

### 对于 CEO（小鸟文书）

此 Skill 是**协议层**，不需要显式调用。它通过以下方式生效：

1. **读取协议文件**: `rules/adaptive-rag-protocol.md` — 获取完整决策树
2. **读取胶囊索引**: `memory/topics/.capsule-index.json` — 获取 42 个胶囊元数据
3. **按决策树执行**: 每次需要记忆时，走 Router → Pre-filter → Search → Rank → CRAG → Generate → Verify

### 对于 SubAgent

SubAgent 在执行任务时：
1. 先判断任务类型 → 决定是否需要检索
2. 需要检索时 → 先做胶囊预筛选
3. 检索结果 → 自行判断质量（CRAG 思维）
4. 输出前 → 自检是否与已知信息矛盾

## 关键文件

| 文件 | 用途 |
|------|------|
| `rules/adaptive-rag-protocol.md` | 完整协议（决策树/分类/bridge/CRAG/L3） |
| `memory/topics/.capsule-index.json` | 42个胶囊的结构化索引 |
| `scripts/build-capsule-index.py` | 重建胶囊索引脚本 |
| `scripts/rag-evaluate.py` | CRAG 质量评估脚本 |

## 快速命令

```bash
# 重建胶囊索引
python3 ~/.openclaw/workspace/skills/adaptive-rag-engine/scripts/build-capsule-index.py

# 评估检索质量
python3 ~/.openclaw/workspace/skills/adaptive-rag-engine/scripts/rag-evaluate.py --query "xxx" --results "result1, result2"
```

## 与其他 Skill 的关系

- **dynamic-rag-capsule** — Context 管理层面的胶囊化（对话太长时压缩）
- **phoenix-memory** — 记忆存储和衰减管理（四层架构）
- **本 Skill** — 检索策略和质量控制（怎么搜、搜到后怎么办）

三者关系：**phoenix-memory 是仓库，dynamic-rag-capsule 是打包器，adaptive-rag-engine 是导航仪**
