---
name: ab-test-runner
description: |
  Design and execute A/B testing experiments for LLM prompts, agent behaviors, and content production.
  Activate when user says "run an AB test", "design an experiment", "做实验", "实验设计",
  "compare X vs Y", or wants to validate a hypothesis via controlled comparison.
---

# AB Test Runner

Run structured A/B experiments: hypothesis → design → execute → archive → update findings.

---

## Workflow

```
Hypothesis → 操作化定义 → 变体设计 → 执行 → 分析 → 归档 → 模板更新
```

---

## Step 1: Hypothesis

**Input from user**: a question or claim to test

**Your task**: Formalize it into the standard format:

```markdown
domain: <prompt|behavior|engineering|content>
variable: <what you're changing>
hypothesis: <具体可检验的因果/差异陈述>
```

**Examples**:
- "自然语言 vs 申论化语言哪个效果好" → `domain: prompt`, `variable: 语言风格`, `hypothesis: 自然语言比申论化语言产出质量更高`
- "语速+15% vs 语速+5%" → `domain: content`, `variable: TTS语速`, `hypothesis: 语速+15%比+5%完播率更高`

**If the user hasn't specified**: Ask 3 questions:
1. 你要改变哪个变量？（A 是什么 vs B 是什么）
2. 你怎么判断哪个更好？（Cooper 主观评判 / 客观指标 / 两者都有）
3. 每组需要多少样本？

---

## Step 2: 操作化定义

Create the experiment manifest before running:

```json
{
  "experiment_id": "hyp-XXX",
  "executed_at": "<ISO timestamp>",
  "domain": "...",
  "variable": "...",
  "hypothesis": "...",
  "n_per_group": <10-30>,
  "rubric": {
    "<维度A>": "0-3 — <标准>",
    "<维度B>": "0-3 — <标准>",
    "<维度C>": "0-3 — <标准>",
    "<篇幅合规>": "0-1 — <标准>"
  },
  "success_criteria": "<假设成立的标准>"
}
```

**Rules**:
- 每组样本 ≥10（低于 10 明确标注"方向性信号，非统计显著"）
- rubric 多维（3 个维度 + 1 个合规项）比单一分数更抗漂移
- 评分方法必须说明：self（自评）/ cross（交叉评）/ external（独立 agent）

---

## Step 3: 变体设计

Define exactly what each variant receives:

```
Variant A — Control 组
- prompt: <完整对照 prompt>
- 样本任务: <3 个代表性任务>

Variant B — Treatment 组  
- prompt: <只改一个变量的 treatment prompt>
- 样本任务: <与 A 完全相同的 3 个任务>
```

**铁律**: 每次只改一个变量。其他所有元素（任务、温度、max_tokens）完全一致。

**质量方差**: 每个 variant 内的任务要有难度差异，确保输出有高/中/低分布。

---

## Step 4: 执行

### 并行 subagent 模板

```
Spawn N 个 subagent（每组一个，或每个任务一个），task 包含：
1. 实验 ID + variant label
2. 完整 rubric（让 agent 知道评分标准）
3. 任务描述
4. 执行指令：生成输出 → 按 rubric 评分 → 记录 self_score + reasoning
5. 输出格式：{id, variant, output, self_score, reasoning}
```

**批量限制**: 每次实验最多并发 3 个 subagent，避免 429 限流

### 交叉评分（如果用 self 评分）

当所有 self 评分完成：
```
再 spawn 1 个 subagent 做盲评：
- 输入：所有输出的匿名版本（A/B label 打乱）
- 任务：对每个输出按 rubric 评分，不知道哪个对应哪个 variant
- 输出：{id, cross_score, reasoning}
```

### 数据收集

汇总所有结果到 `memory/experiments/auto-ab-results.json`：

```json
{
  "experiment_id": "hyp-XXX",
  "executed_at": "...",
  "variant_a": { "label": "...", "samples": N, "avg_score": X.X },
  "variant_b": { "label": "...", "samples": N, "avg_score": X.X },
  "winner": "A|B|none",
  "conclusion": "..."
}
```

---

## Step 5: 分析

根据结果判断：

| 条件 | 结论 |
|------|------|
| A 显著优于 B（效应量大） | `confirmed` |
| B 显著优于 A | `refuted`（假设方向错误） |
| 部分维度成立 | `partially_confirmed` |
| 无差异，样本够 | `inconclusive` |
| 样本 <10 | `insufficient_sample` |

**计算均值差异 + 效应量方向**，给出具体结论。

---

## Step 6: 归档

### 写入 hypotheses registry

`memory/experiments/auto-ab-hypotheses.json`：追加/更新对应 hyp 条目

### 写入详细分析

`memory/experiments/hyp-XXX.md`：包含完整 rubric、样本统计、结论、后续实验建议

### 更新模板

`memory/experiments/AB-test-design-template.md`：
- 新发现 → 追加到 Section 10 "核心发现"
- 新坑点 → 追加到 Section 11 "已知坑点"

---

## Step 7: 回报给 Cooper

简洁回报格式：

```
实验 hyp-XXX | <domain>
假设: <一句话假设>
结果: A 胜 / B 胜 / 无差异
核心发现: <一句话>
结论: <Cooper 是否应该改变现有做法>
下一步: <如果要继续，下一步是什么>
```

---

## 关键配置

- **数据文件**: `memory/experiments/auto-ab-results.json`
- **假设注册表**: `memory/experiments/auto-ab-hypotheses.json`  
- **模板**: `memory/experiments/AB-test-design-template.md`
- **坑点**: `memory/experiments/AB-test-design-template.md` Section 11

---

## 已知坑点（执行前必读）

1. **API token=0**: 执行前健康检查，失败立即重试
2. **自评膨胀**: 不依赖 self_score 作为唯一指标，用 cross_score 校正
3. **迭代拐点**: 超过 3 轮迭代质量下降，报告时标注
4. **输出非确定性**: 每组至少 10 样本抵消随机性

---

*基于 Batch 2（6实验，190样本）+ Hypothesis系列（5假设）实战经验*
