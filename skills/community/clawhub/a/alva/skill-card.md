## Description:

Alva helps agents answer financial data questions, analyze markets, backtest strategies, and build Alva playbooks and dashboards using financial data, cloud analytics, and trading workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaxxjj](https://clawhub.ai/user/jaxxjj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and finance-focused agents use this skill to retrieve market data, build research workflows, create dashboards and playbooks, run backtests, and manage trading-related Alva workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad Alva account access across financial data, cloud scripts, scheduled automations, public releases, memory personalization, and trading-related workflows.

Mitigation: Install only after confirming that level of access is acceptable, and require explicit user confirmation before publishing, granting public access, enabling push alerts, or executing non-paper trading actions.

Risk: The setup flow includes global installation or upgrade of the Alva CLI package.

Mitigation: Review the package installation behavior and avoid automatic updates to unpinned packages in controlled environments.

Risk: The skill can use persistent memory and third-party secrets to personalize finance workflows.

Mitigation: Keep secrets in Alva Secret Manager, do not place secret values in generated files or released assets, and inspect memory contents periodically.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaxxjj/skills/alva)
- [Alva Language Guidelines](references/language.md)
- [Alva Feed SDK](references/feed-sdk.md)
- [Altra Trading](references/altra-trading.md)
- [Deployment](references/deployment.md)
- [Secret Manager](references/secret-manager.md)
- [Release API](references/api/release.md)
- [Trading API](references/api/trading.md)
- [Push Subscriptions API](references/api/push-subscriptions.md)
- [Remix Workflow](references/remix-workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with code blocks, commands, configuration steps, and generated playbook or feed files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide authenticated Alva data queries, dashboards, scheduled automations, playbook releases, push notifications, and trading-related workflows.]

## Skill Version(s):

1.7.1 (source: server release evidence; artifact frontmatter says v1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
