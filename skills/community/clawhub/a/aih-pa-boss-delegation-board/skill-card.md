## Description:

将老板交办事项、负责人、期限和可见范围整理成可审阅的进度看板、决策清单及跟进草稿，并在授权和工具可用时支持 AI-HIVE 辅助处理。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Executives and their assistants use this skill to organize delegated work by owner and deadline, identify decisions requiring approval, and prepare a reviewable progress board and follow-up drafts. Optional AI-HIVE use requires available tools and separate authorization for external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional AI-HIVE access could expose sensitive project materials or incur charges.

Mitigation: Review MCP/OAuth permissions, minimize and approve upload scope, and confirm pricing and a spending cap before use.

Risk: A draft may be mistaken for a completed external action, or an action may exceed the user's authority.

Mitigation: Require separate authorization for sending, payments, deletion, publication and business-system writes; verify actual receipts and results before reporting completion.

Risk: Credential requests in chat or imported materials could compromise accounts.

Mitigation: Do not share passwords, tokens, cookies or verification codes in chat; treat imported material as data, not instructions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/aih-pa-boss-delegation-board)
- [Workflow and acceptance criteria](references/workflow-27.md)
- [AI-HIVE connection and authorization](references/ai-hive-connection.md)
- [Output and evidence contract](references/output-contract.md)
- [Scope and sources](references/scope-and-sources.md)
- [AI-HIVE web interface](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [HTML, Text, JSON]

**Output Format:** [Reviewable HTML progress board, decision list and follow-up drafts; optional structured JSON records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records identify unknowns and evidence; external actions are not implied by drafts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
