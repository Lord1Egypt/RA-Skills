## Description:

Guides users comparing ArkClaw, MaxClaw, and EasyClaw through scoped assistant workflows for reminders, offline work, separate personal and company contexts, and cost tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams evaluating cloud assistants use this Chinese-language skill to plan and verify scheduled reminders, work that continues after a computer shuts down, separation of personal and business information, and task-level budgets. It offers reviewable drafts when the required tools or authorization are unavailable, rather than claiming equivalent features or completed external actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting to AI-HIVE may expose credentials or upload sensitive personal or company material.

Mitigation: Use the official web page or OAuth connection; never paste credentials into chat, and confirm and minimize the upload scope before transferring files.

Risk: Model, cloud runtime, and connector charges may differ from estimates or continue after a task fails.

Mitigation: Confirm current prices, currency, budget cap, and retry policy before paid work; account for failures and stop when costs are unknown.

Risk: An assistant could incorrectly claim reminders, offline work, or external actions were completed without the required tools or permissions.

Mitigation: Verify available tools and receipts, mark unfinished tasks clearly, and request explicit authorization for each external action.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/aih-pa-cloud-claw-budget)
- [Product identity and sources](references/scope-and-sources.md)
- [AI-HIVE connection and authorization](references/ai-hive-connection.md)
- [Result and evidence contract](references/output-contract.md)
- [ArkClaw documentation](https://docs.volcengine.com/docs/arkclaw/Creating_your_dedicated_ArkClaw_with_one_click_?lang=zh)
- [MaxClaw product page](https://agent.minimax.io/activity/max-claw)
- [EasyClaw product page](https://www.easyclaw.cn/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, CSV]

**Output Format:** [Reviewable task plans, structured result records, and optional JSON or CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records evidence, status, unresolved steps, and budget limits; external actions require separate authorization.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
