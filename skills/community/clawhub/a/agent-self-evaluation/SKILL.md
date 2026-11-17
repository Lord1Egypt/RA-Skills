---
name: agent-self-evaluation
description: "Self-evaluate task completion across 5 axes �� accuracy, completeness, clarity, actionability, conciseness. Use when completing any task to score output quality and provide evidence for low scores."
metadata:
  origin: ECC agent-self-evaluation
---

# Agent Self-Evaluation �?5 轴自评估

任务完成后，对输出进行结构化自评。这不是通过/失败门控，而是刻意反思步骤，在用户之前捕获遗漏、标记过度自信�?surfaced 改进区域�?
## 触发条件

- 编写�?3+ 文件�?50+ 行代�?- 完成多步骤工作流（实�?�?测试 �?审查�?- 调试会话涉及 3+ 次尝�?- 产出设计文档、架构决策或书面分析
- 用户�?那有多好�?�?评价一下你自己"

## 5 个评估轴

| �?| 问题 | 捕获什�?|
|-----|------|----------|
| **准确�?* | 事实、声明和输出正确吗？ | 幻觉、错�?API 名称、不正确语法、错误陈�?|
| **完整�?* | 覆盖了用户要求的所有内容吗�?| 遗漏的边界情况、未处理的错误路径、遗忘的需求、跳过的子任�?|
| **清晰�?* | 解释可理解且结构良好吗？ | 混淆的解释、无定义的术语、缺少上下文、冗�?|
| **可操作�?* | 用户可以立即基于输出行动吗？ | 模糊建议、缺少步骤�?你应�?X"但不展示如何做、无验证路径 |
| **简洁�?* | 使用了最少必要的�?token 吗？ | 冗余、过度解释、逐字重复用户问题、填充内�?|

## 评分标准

```
5 �?卓越：无合理改进可能
4 �?良好：只有小瑕疵，无实质性差�?3 �?足够：满足请求但至少一个轴有明显弱�?2 �?弱：有明确差距影响可用性正确�?1 �?差：根本未满足请求或包含重大错误
```

## 证据规则

**每个低于 5 分的必须引用具体证据�?*

3 分不能只�?可以更好"——必须说�?*缺少什�?*�?*错在哪里**�?
口号�?*"展示差距，不只是命名它�?**

## 工作�?
### Step 1: 收集原始材料

收集要评估的内容�?
```
- 原始用户请求（从对话中回读）
- 最终响�?输出（可交付物）
- 验证正确性的任何工具输出（测试结果、退出码、lint 输出�?- 任务期间收到的任何用户反馈（纠正�?再试一�?�?那不�?�?```

### Step 2: 独立评分每个�?
逐个处理 5 个轴。对每个�?
1. 阅读轴问�?2. 在输出中查找证据（或缺乏证据�?3. 分配分数 1-5
4. 如果分数 < 5，写一句改进说明引用差�?
**不要**先在心中平均分数然后反向工作。每个轴新鲜评分�?
### Step 3: 产出评估报告

报告必须包括�?
```
- 一行摘�?- 5 轴评分卡（每轴的分数 + 证据�?- 总分（简单平均，四舍五入�?1 位小数）
- 按影响排序的 1-3 个具体改�?- 自检�?用户会同意这个评估吗�?
```

### Step 4: 应用改进

如果任何轴评�?3 或以下：

1. 说明你会怎么做不�?2. 如果差距可在 < 30 秒内修复（缺少链接、不清晰措辞），立即修复
3. 如果差距需要返工，明确标记�?这个轴评�?[原因] 因为 [证据]。用 [具体修复] 重新运行可能会提高到 [分数]�?

## 报告模板

```markdown
## Self-Evaluation Report

**Task**: {task description}
**Overall Score**: {average}/5

### Scorecard

| Axis | Score | Evidence |
|------|-------|----------|
| Accuracy | {1-5} | {specific evidence or "No gaps found"} |
| Completeness | {1-5} | {specific evidence or "No gaps found"} |
| Clarity | {1-5} | {specific evidence or "No gaps found"} |
| Actionability | {1-5} | {specific evidence or "No gaps found"} |
| Conciseness | {1-5} | {specific evidence or "No gaps found"} |

### Top Improvements

1. {highest impact improvement}
2. {second highest}
3. {third highest}

### Self-Check

Would the user agree with this assessment? {Yes/No, why}
```

## 示例

### 示例 1: 良好评估�?+ 分）

```markdown
## Self-Evaluation Report

**Task**: Add retry logic to HTTP client
**Overall Score**: 4.6/5

### Scorecard

| Axis | Score | Evidence |
|------|-------|----------|
| Accuracy | 5 | All API calls correct. Verified: retries use exponential backoff. No hallucinated methods. |
| Completeness | 4 | Covered happy path + 3 error cases. Missing: timeout handling for hung connections. |
| Clarity | 5 | Code comments explain backoff formula. PR description links to incident. |
| Actionability | 5 | Single merge. No follow-up tasks. Tests pass. |
| Conciseness | 4 | 47 lines total. The retry loop could be extracted into a helper to drop ~8 lines. |

### Top Improvements

1. Add timeout handling for hung connections (Completeness)
2. Extract retry loop into helper function (Conciseness)

### Self-Check

Would the user agree? Yes �?one clear gap (timeout) identified, fix is straightforward.
```

### 示例 2: 弱评估（2-3 分）

```markdown
## Self-Evaluation Report

**Task**: Add retry logic to HTTP client
**Overall Score**: 2.8/5

### Scorecard

| Axis | Score | Evidence |
|------|-------|----------|
| Accuracy | 2 | Used urllib3 which doesn't match our httpx-based codebase. Wrong library. |
| Completeness | 3 | Works for GET. POST/PUT not handled (user said "all HTTP requests"). |
| Clarity | 4 | Code is readable. Good variable names. |
| Actionability | 2 | "Add tests" mentioned but no test file created. User has to write tests before merging. |
| Conciseness | 3 | 120 lines. Retry config duplicated in 3 places instead of one shared RetryConfig object. |

### Top Improvements

1. Switch to httpx transport (Accuracy �?wrong library)
2. Extend to all HTTP methods (Completeness �?POST/PUT missing)
3. Consolidate retry config into single object (Conciseness �?3x duplication)

### Self-Check

Would the user agree? Yes �?wrong library is critical, must fix before merging.
```

## 反模�?
### "Everything is a 5"

```
FAIL: Accuracy:    5 �?All good.
   Completeness: 5 �?Everything covered.
   Clarity:      5 �?Clear.
```

无证据引用。这是自我祝贺，不是评估。真正的 5 需要证明没有改进空间�?
### Over-penalizing for scope creep

```
FAIL: Completeness: 2 �?Didn't handle WebSocket connections or gRPC streaming (user didn't ask for these)
```

只针对用户实际请求的内容评估，不是你可能额外构建的内容�?
### Using the evaluation to re-litigate

```
FAIL: "As I said earlier, this approach is wrong. Score: 1"
```

评估是关于交付的输出，不是关于重新争论已经做出的设计决策。如果方法错误，应该在交付前捕获�?
### Mixing personal preference with objective gaps

```
FAIL: "Score: 3. I don't like Python decorators."
```

"不喜�?不是证据。引用具体的可读性、可测试性或正确性问题，或保持分�?4+�?
## 最佳实�?
- **评估输出，不是过程�?* 用户关心你交付了什么，不是你花了多少次迭代�?- **每个弱轴一个改进�?* 不要为一个轴列出 5 件事——选择最高影响差距�?- **将改进与用户影响绑定�?* "缺少错误处理意味着用户�?API 调用会静默崩�? �?"添加错误处理" 更好�?- **具体说明"修复"的样子�?* "用为重试配置�?httpx 传输重新运行" �?"修复库问�? 更好�?- **使用工具输出作为证据�?* 如果测试通过，引用它们。如�?lint 干净，引用它。不要猜测——grep 证明�?- **如果找不到任何差距，更努力尝试�?* 5 个轴的完美分数很罕见。问�?如果我是用户，这个输出的什么会让我烦恼�?

## 与现有规则的关系

| 现有规则 | 本技能增�?|
|---------|-----------|
| SOUL.md 规则 8: 输出前重复检�?| 5 轴系统化评估 |
| SOUL.md 规则 9: 状态管�?| 证据规则（低�?5 分必须证据） |
| SOUL.md 规则 10: 输出长度控制 | 简洁性轴 |
| coding-framework Step 7: 收尾检�?| 结构化评分卡 |

## 简化使�?
不需要每次都完整报告。对于快速检查：

```markdown
## Quick Self-Check

- Accuracy: {1-5} �?{one-line evidence}
- Completeness: {1-5} �?{one-line evidence}
- Clarity: {1-5} �?{one-line evidence}
- Actionability: {1-5} �?{one-line evidence}
- Conciseness: {1-5} �?{one-line evidence}

**Overall**: {average}/5
**Top fix**: {highest impact improvement}
```

---

*5 轴自评估：在用户之前捕获遗漏，用证据说话�?
