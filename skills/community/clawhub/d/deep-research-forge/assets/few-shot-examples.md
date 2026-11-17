# Few-Shot Examples

This file provides compact positive and negative examples to calibrate
deep-research-forge output quality. Use these as reference, not as rigid templates.

---

## ✅ Positive Example: Minimal Output (research-orientation)

> User: "研究一下 Cursor 这个产品"

```markdown
# Research Brief: Cursor IDE

## 研究问题
Cursor 是什么，为什么快速增长，是否仍值得关注？

## 一句话结论
Cursor 是 AI-first 代码编辑器，通过深度集成 LLM 能力获得快速采用；值得关注但竞争压力在增加。[E-001]

Confidence: medium

## 证据底座
- 基于 VS Code fork 构建，原生 AI 集成 [E-001]
- 报道融资 $60M Series A，估值 $400M 但未经独立证实 [E-002]
- 用户称赞 tab 补全和多文件编辑 [E-003]

Evidence window: 2023–2026

## 下一步
季度监控 Copilot 功能路线图；如有企业采用数据可重新评估。
```

**为什么好**：先给结论，证据有 ID 追溯，标注置信度和证据窗口，
下一步具体且可操作。没有过度展开。

---

## ✅ Positive Example: Decision Brief (excerpt)

> User: "我们团队要不要采用这个可观测性厂商？"

```markdown
## Verdict: EXPERIMENT

Confidence: medium

## Key Assumptions
- 团队规模 < 50 人
- 当前无统一可观测性平台
- 预算允许 3 个月试点

## Evidence Supporting
- 功能覆盖日志、指标、链路追踪 [E-010]
- 定价透明，按用量计费 [E-011]

## Evidence Weakening
- 缺少大规模生产环境验证 [E-012]
- 社区活跃度低于竞品 [E-013]

## Reversal Conditions
- 试点期间 P99 延迟 > 500ms → 重新评估
- 竞品在 6 个月内发布等效功能 → 重新比较

## Next Action
申请 3 个月试点，设定 P99 延迟 < 200ms 和数据丢失率 < 0.1% 的成功标准。
```

**为什么好**：verdict 匹配证据强度（不是 GO），假设明确，
反转条件可测量，下一步比不可逆决策小。

---

## ❌ Negative Example: Over-templated Output

```markdown
# Deep Research Report: [Product Name]

## Executive Summary
This is a revolutionary, game-changing product that leverages synergistic
AI capabilities to deliver world-class performance.

## Timeline
- 2023: Founded
- 2024: Launched
- 2025: Grew

## Competitive Matrix
| Feature | Product A | Product B |
|---------|-----------|-----------|
| Feature 1 | ✓ | ✗ |
| Feature 2 | ✓ | ✓ |

## Conclusion
The product is cutting-edge and disruptive. We recommend adopting it.
```

**为什么差**：
- 空话标记词：revolutionary, game-changing, synergistic, world-class, cutting-edge, disruptive
- 时间轴只列日期，没有因果解释
- 竞品矩阵只是功能勾选，没有用户选择逻辑
- 结论没有证据 ID、置信度、反转条件
- 没有证据窗口声明
- verdict 是 GO 但没有证据支撑

---

## ❌ Negative Example: Fabricated Research

```markdown
## Survey Results

We surveyed 500 developers and found that 87% prefer Cursor over VS Code.
Interviews with 20 CTOs revealed that enterprise adoption is accelerating.
```

**为什么差**：
- 编造了不存在的调研数据（skill 明确禁止 fabricate surveys/interviews）
- 没有来源、没有方法论、没有样本量说明
- 应改为：设计调研计划，标注为 gap
