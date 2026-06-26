---
name: research_question_parser
description: 解析用户的自然语言临床科研问题，输出结构化研究参数（研究类型、终点、变量、推荐workflow）。当用户提出一个科研问题并需要将其转为结构化任务时触发。
---

# 研究问题解析 Skill

## 何时使用

当用户输入一个自然语言的临床科研问题（如「评估胃癌术后感染风险」「分析某某治疗方案差异」），需要将其解析为结构化研究任务时，使用本 skill。

## 执行步骤

### 1. 上报开始

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"research-question-parser","display_name":"研究问题解析","status":"running","message":"正在解析研究问题，提取结构化参数..."}'
```

### 2. 读取数据并输出结果

读取文件 `/home/ubuntu/workspace/demo/mock_data/task_create.json`。

根据其中的数据，向用户展示以下内容（使用清晰的格式化输出）：

- **原始研究问题**：`task_input.raw_query`
- **结构化参数**：时间范围、疾病领域、手术类型、主要终点、对比分组、输出偏好（来自 `task_form`）
- **任务解析预览**：研究类型、目标人群、主要结局、候选变量列表（来自 `task_parse_preview`）
- **推荐 Workflow**：列出推荐的执行步骤（来自 `workflow_preview`）
- **推荐 Skills**：如果数据中有 `recommended_skills`，一并展示

### 3. 上报完成

```bash
curl -s -X POST http://localhost:5001/api/report \
  -H "Content-Type: application/json" \
  -d '{"skill":"research-question-parser","display_name":"研究问题解析","status":"completed","message":"研究问题解析完成，已生成结构化任务参数与推荐 Workflow"}'
```

## 输出要求

- 使用结构化格式（表格或分段列表）展示，不要输出原始 JSON
- 如果用户的问题与胃癌/手术后感染无关，仍使用 mock 数据演示流程，但说明这是 demo 数据
