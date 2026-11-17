---
name: ab-test-agent-workflow
version: 1.1.0
description: >
  多agent双盲 A/B 测试工作流。对多个 AI model/Agent 进行多轮次、双盲对照测试。
  核心role：coordinate者（Coordinator）、受测者 A/B（Contestant）、评测者（Judge）。
  trigger场景："A/B 测试"、"双盲测试"、"比较 AI model"、"model评测"、"测试工作流"、
  "compare models"、"blind test"、"multi-round evaluation"。
---

# A/B Test Agent Workflow

多agent双盲 A/B 测试工作流 — coordinate者主导、受测者并行、评测者盲评。

## 何时使用

✅ 用户说以下内容时trigger本 Skill：
- "A/B 测试"
- "双盲测试"
- "比较 AI model"
- "model评测"
- "run a blind test"

❌ 不适用：单modelassess、简单问答、快速原型verify。

## 工作流架构

```
┌─────────────────────────────────────────────────────────┐
│                   coordinate者 (Coordinator)                   │
│  ① 接收任务 + 轮次配置                                   │
│  ② 向 Contestant A 发送 Prompt                          │
│  ③ 向 Contestant B 发送 Prompt                          │
│  ④ 收集输出 → 匿名化为"plan1"/"plan2"                    │
│  ⑤ 向 Judge 发送匿名plan                                 │
│  ⑥ 收集评分 → record结果                                   │
│  ⑦ 重复 ④-⑥ N 轮                                       │
│  ⑧ 汇总 → 揭示身份 → 输出结构化report                      │
└─────────────────────────────────────────────────────────┘
        ↓                    ↓                    ↓
  ┌──────────┐        ┌──────────┐        ┌──────────┐
  │Contestant│        │Contestant│        │  Judge   │
  │    A     │        │    B     │        │  (盲评)  │
  └──────────┘        └──────────┘        └──────────┘
```

## roleDefinition

### 1. coordinate者（Coordinator）— 主会话
- 接收用户输入（任务、轮次、受测model/Rubric）
- 调度子 Agent 并收集输出
- execute匿名化handle
- 汇总结果，输出最终report

### 2. 受测者 A/B（Contestant A / B）
- 各接收相同的 Prompt
- 独立生成输出
- 不知道自己正在与谁比较
- 由 `sessions_spawn` 隔离execute（`runtime=subagent`）

### 3. 评测者（Judge）
- 仅收到"plan1"和"plan2"（不知道来源）
- 根据 Rubric 打分
- 提供评语和胜出方建议
- 由 `sessions_spawn` 隔离execute（`runtime=subagent`）

## execute方式

### 方式1：纯 AI coordinate（推荐）
直接在本会话中按工作流execute，无需脚本。

**Prompt 模板（发给 Contestant A — 普通任务）：**
```
你是 Contestant A。请完成以下任务，只输出结果，不要Description你是谁、不要加前缀：

[TASK]

输出格式（严格遵守）：
[CONTENT_A]
[你的完整输出]
[/CONTENT_A]
```

**Prompt 模板（发给 Contestant B — 普通任务）：**
```
你是 Contestant B。请完成以下任务，只输出结果，不要Description你是谁、不要加前缀：

[TASK]

输出格式（严格遵守）：
[CONTENT_B]
[你的完整输出]
[/CONTENT_B]
```

**Prompt 模板（发给 Contestant A — 代码生成任务）：**
```
你是 Contestant A。请完成以下任务。

任务：[TASK]

⚠️ 重要要求：先输出完整代码，再输出运行结果。代码必须在 [CONTENT_A] 标签内完整呈现，即使超时也优先返回代码。

输出格式（严格遵守）：
[CONTENT_A]
【代码】
```python
[你的完整代码]
```

【运行结果】
[如有，运行结果]
[/CONTENT_A]
```

**Prompt 模板（发给 Contestant B — 代码生成任务）：**
```
你是 Contestant B。请完成以下任务。

任务：[TASK]

⚠️ 重要要求：先输出完整代码，再输出运行结果。代码必须在 [CONTENT_B] 标签内完整呈现，即使超时也优先返回代码。

输出格式（严格遵守）：
[CONTENT_B]
【代码】
```python
[你的完整代码]
```

【运行结果】
[如有，运行结果]
[/CONTENT_B]
```

**Prompt 模板（发给 Judge）：**
```
你是1位严格公正的评测专家。请对以下两个匿名plan进行打分。

评测任务：[TASK]

评分维度（满分 10 分）：
1. 准确性（答案是否正确）
2. 完整性（是否覆盖所有要点）
3. 表达质量（语言是否流畅、清晰）
4. 创意/深度（是否有独到见解）

plan1：
[SOLUTION_1]

plan2：
[SOLUTION_2]

输出格式（严格遵守）：
[SCORES]
plan1-准确性: X/10（简短理由）
plan2-准确性: X/10（简短理由）
plan1-完整性: X/10（简短理由）
plan2-完整性: X/10（简短理由）
plan1-表达质量: X/10（简短理由）
plan2-表达质量: X/10（简短理由）
plan1-创意/深度: X/10（简短理由）
plan2-创意/深度: X/10（简短理由）
[/SCORES]
[TOTAL_A]4项得分之和[/TOTAL_A]
[TOTAL_B]4项得分之和[/TOTAL_B]
[WINNER]plan1 或 plan2 或 平局[/WINNER]
[COMMENT]总体评语（150字以内）[/COMMENT]
```

### 方式2：脚本驱动
```
python scripts/runner.py --prompt "写1首关于春天的诗" --rounds 3 --model-a claude-sonnet-4 --model-b gpt-4o
```

## executeprocess详解

### 第 1 步：接收配置
```
用户输入：
  - 任务 Prompt
  - 测试轮次（默认 3）
  - 评分维度（可自Definition Rubric）
  - 可选：指定受测model
```

### 第 2 步：双盲分发
```
Round N：
  → 向 Contestant A 发送 Prompt（A 的专属版本）
  → 向 Contestant B 发送 Prompt（B 的专属版本）
  并行等待，两方互不知道对方的存在
```

### 第 3 步：匿名化
```
收集 A 的输出 → 记为 S1
收集 B 的输出 → 记为 S2
随机决定展示顺序（防顺序bias）
→ 发给 Judge
```

### 第 4 步：盲评
```
Judge 收到 S1、S2（无来源信息）
按 Rubric 逐项打分
输出分数 + 评语 + 胜出方
```

### 第 5 步：结果record
```
Round N 结果：
  S1 = [A 的输出]
  S2 = [B 的输出]
  Judge 分数：S1=X, S2=Y
  胜出方：Z
```

### 第 6 步：汇总
```
所有轮次完成后：
  - 汇总各轮得分
  - 计算胜率
  - 揭示身份
  - 输出最终report
```

## 结果report模板

```json
{
  "test_summary": {
    "task": "...",
    "rounds": 3,
    "contestant_a": "Model A / Agent A",
    "contestant_b": "Model B / Agent B",
    "rubric": ["准确性", "完整性", "表达质量", "创意"]
  },
  "rounds": [
    {
      "round": 1,
      "contestant_a_output": "...",
      "contestant_b_output": "...",
      "judge_scores": {
        "contestant_a": [9, 8, 9, 7],
        "contestant_b": [8, 9, 8, 8]
      },
      "winner": "contestant_a",
      "judge_comment": "..."
    }
  ],
  "final_result": {
    "total_score_a": 83,
    "total_score_b": 80,
    "wins_a": 2,
    "wins_b": 1,
    "winner": "Model A",
    "confidence": "中（各胜 1 轮，建议增加轮次）"
  }
}
```

## 文件结构

```
ab-test-agent-workflow/
├── SKILL.md                    ← 本文件（工作流Description）
├── scripts/
│   ├── runner.py               ← 多轮驱动引擎 + 自测模式
│   ├── judge_prompts.py       ← Judge 提示词build + 解析
│   └── anonymizer.py          ← 匿名化工具（过滤身份标识）
└── references/
    ├── rubric_templates.md      ← 各任务类型评分模板
    └── workflow_guide.md        ← 详细executestep指南
```

## 自测命令

```bash
# 自测模式（无需 subagent，verify工作流逻辑）
python scripts/runner.py --test --rounds 3

# 预览 Prompt（不实际execute）
python scripts/runner.py --prompt "写1首关于春天的诗" --skip-spawn
```

## Rubric 模板速查

| 任务类型 | 推荐评分维度 |
|---------|------------|
| 写作/文案 | 准确性、完整性、表达、创意 |
| 代码生成 | 正确性、可读性、效率、security性 |
| 逻辑推理 | 准确性、推理深度、解释清晰度 |
| 知识问答 | 准确性、完整性、可信度 |
| 创意写作 | 原创性、文学性、主题契合度 |

## 已知问题与handle技巧

### 超时handle
- **现象**：子 Agent 在 57s 超时边缘可能只输出运行日志，未返回完整代码。
- **resolve**：代码任务 Prompt 中明确要求"**先输出完整代码，再输出运行结果**"，即使超时也优先返回代码。
- **超时重试**：Judge 如果在 60s 内无输出，可重新 spawn 1个新的 Judge session。

### 匿名化risk
- 如果输出内容包含参赛者名称（如"作为 Claude"）或明确署名，Judge 容易猜出来源。
- **resolve**：使用 `scripts/anonymizer.py` 预handle，移除身份标识词（Claude/GPT/Gemini/参赛者A/参赛者B 等）。
- Judge prompt 中明确声明："你不知道plan1来自哪个参赛者"。

### 评分解析失败
- 如果 Judge 输出格式不standard（缺少 `[SCORES]` 等标签），解析器会 fallback 到智能提取。
- **建议**：Judge prompt 中用 `[SCORES]...[/SCORES]` 严格Constraint输出格式。

### 同model测试
- 使用相同model（如同为 qclaw/modelroute）测试时，输出相似度高，Judge 倾向于判平。
- 这是正常现象，不代表工作流有问题。
- **建议**：对比不同model时才容易拉开差距。
