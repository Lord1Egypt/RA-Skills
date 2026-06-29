---
name: error-message-improver
description: >-
  帮助用户处理“Validated demand: Users and support teams need clearer error messages that explain what failed, why it failed, and what action to take next. This requirement is supported by 12 separate online signals across 4 source families, so it represents broader demand rather than a single isolated request.”。当用户提出 work-productivity, error messages, debugging, user feedback, support，或需要围绕该需求获得实用流程、产物、检查清单、分析或实现支持时使用。
---

# Error Message Improver

## 需求

使用这个技能帮助以下用户群体：application developers, support teams, SaaS operators, and users who lose time when vague errors block troubleshooting

> Validated demand: Users and support teams need clearer error messages that explain what failed, why it failed, and what action to take next. This requirement is supported by 12 separate online signals across 4 source families, so it represents broader demand rather than a single isolated request.

需求评分：100/100（需求强度 `70/70`，本地可执行性 `30/30`）。
证据：12 条信号，覆盖 4 个来源类型。

如需查看来源证据、执行计划或评审标准，请阅读 `references/requirement-plan.md`。

## 工作流程

1. 重新说明用户想要的结果、限制、已有输入和成功标准。
2. 创建简洁的工作计划、模板、自动化思路或决策辅助，减少手动协调。
3. 只有当缺失信息会明显改变输出时才提问；否则先做合理假设并继续推进。
4. 保持本地硬件友好：优先使用脚本、模板、检查清单、小模型或 CPU 可承受的流程，避免依赖云端专用资源或大规模训练。
5. 产出用户需要的文档、流程、清单、分析、代码修改或决策支持。
6. 对照成功标准检查结果，并列出剩余风险或后续事项。

## 预期输出

- 针对用户当前情境的定制回答或产物。
- 当任务可复用时，提供检查清单或工作流程。
- 说明结果如何被检查的验证备注。

## 验证

- 输出直接回应发现的原始需求。
- 用户不需要阅读原始来源帖子也能采取行动。
- 假设、限制和所需输入清晰可见。
- 在有帮助时，最终回复包含简短的使用说明或下一步建议。

## 触发方式

关键词：`work-productivity`, `error messages`, `debugging`, `user feedback`, `support`, `troubleshooting`

示例触发句：

- `Help me Users and support teams need clearer error messages that explain what failed, why it failed, and what action to take nex.`
- `I need a practical workflow for Users and support teams need clearer error messages that explain what failed, why it failed, and what action to take nex.`
- `Use $error-message-improver to handle Users and support teams need clearer error messages that explain what failed, why it failed, and what action to take nex.`
