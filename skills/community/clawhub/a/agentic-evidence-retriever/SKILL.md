---
name: evidence_retriever
description: 检索 PubMed 文献、临床指南与试验注册信息，提取证据摘要并生成 Research Grounding 建议（推荐终点定义、时间窗、混杂因素）。当用户需要做文献检索或证据 grounding 时触发。
---

# 证据检索与 Grounding Skill

## 何时使用

当用户需要**单独执行**文献/证据检索时使用，例如：
- 「帮我检索胃癌术后感染相关文献」
- 「查找相关的临床指南和试验」
- 「做一下 research grounding」

如果是完整任务流程的一部分，则由 task-planner 调度，无需用户单独触发。

## 执行步骤

### 1. 上报开始

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"evidence-retriever","display_name":"证据检索与 Grounding","status":"running","message":"正在检索 PubMed、指南库与试验注册信息..."}'
```

### 2. 读取数据并输出

读取 `/home/ubuntu/workspace/demo/mock_data/evidence.json`，向用户展示：

- **证据来源统计**：指南 X 条、PubMed X 条、试验 X 条
- **证据列表**：每条显示类型标签、标题、来源、年份、关键结论
- **证据摘要详情**：选中条目的详细摘要、关键因素、推荐用途
- **Grounding 建议**：
  - 推荐主要终点
  - 推荐时间窗
  - 候选混杂因素列表
  - 注意事项

### 3. 上报完成

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"evidence-retriever","display_name":"证据检索与 Grounding","status":"completed","message":"已检索 6 条相关证据，完成研究边界 Grounding"}'
```
