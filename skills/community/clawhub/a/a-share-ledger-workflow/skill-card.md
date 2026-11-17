## Description:

A股投研工作流覆盖方向研究、产业链分析、选股跟踪、买入前核验、持仓台账与交易复盘。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangclaw2026-png](https://clawhub.ai/user/yangclaw2026-png)

### License/Terms of Use:

MIT

## Use Case:

外部投资研究者可用它组织中国 A 股的端到端研究流程、维护可追溯的候选与持仓台账，并复盘已完成的交易。它不代替用户作出投资决定或执行交易。

### Deployment Geography for Use:

China (Mainland A-share market)

## Known Risks and Mitigations:

Risk: Insecure connections could expose Feishu credentials.

Mitigation: Restore certificate verification before enabling integrations, and verify Feishu and email destinations.

Risk: The watchdog may monitor unrelated tasks.

Mitigation: Restrict it to explicitly selected investment jobs before enabling it.

Risk: External helper behavior and live service behavior remain unverified.

Mitigation: Review the separate writer and mailer helpers and verify integrations before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yangclaw2026-png/skills/a-share-ledger-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Configuration, Code, Shell commands]

**Output Format:** [Markdown reports and ledgers, JSON or YAML configuration, and Python or shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update research ledgers, templates, and reports; does not place trades.]

## Skill Version(s):

1.0.5 (source: frontmatter; server-resolved release: 1.0.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
