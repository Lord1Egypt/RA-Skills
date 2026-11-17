## Description:

Helps assess partner compliance risk by organizing checks for business-record changes, litigation, dishonest-debtor listings, risk scoring, and Feishu-style alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Employees in compliance, procurement, or legal teams use this skill to query or organize monitoring of suppliers and customers for Chinese business-record and legal-risk signals. It supports single-company review, bulk import, risk scoring, alert drafting, and monthly report drafting.

### Deployment Geography for Use:

China-focused; non-China company monitoring requires separately configured data sources.

## Known Risks and Mitigations:

Risk: Users may mistake the artifact for a working compliance monitor even though server security evidence identifies it as incomplete.

Mitigation: Review before installing and add real data-source queries, tested Feishu integration, scheduling, alerting, and report generation before relying on it for monitoring.

Risk: API keys, Feishu tokens, alert recipients, and partner-list storage may expose sensitive business or personal data if deployed without controls.

Mitigation: Limit credential scopes, define who receives alerts, confirm partner-list storage with data owners, and document retention and deletion controls.

## Reference(s):

- [Risk rules](references/risk-rules.md)
- [Data sources](references/data-sources.md)
- [Notification templates](references/notification-templates.md)
- [National Enterprise Credit Information Publicity System](https://www.gsxt.gov.cn/)
- [China Judgments Online](https://wenshu.court.gov.cn/)
- [Dishonest Judgment Debtors Query](https://zxgk.court.gov.cn/shixin/)
- [State Taxation Administration](https://www.chinatax.gov.cn/)
- [Qichacha Open API](https://openapi.qcc.com/)
- [Tianyancha Open Platform](https://open.tianyancha.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, terminal text, JSON summaries, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference CSV partner imports, commercial API keys, Feishu table fields, alert templates, and monthly report fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
