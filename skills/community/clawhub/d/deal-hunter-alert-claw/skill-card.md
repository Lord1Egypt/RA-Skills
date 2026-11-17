## Description:

商业捡漏预警虾 monitors configured deal, real estate, auction, and procurement sources, evaluates discounts and risks, and returns alert-ready results.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to define monitoring rules for low-priced second-hand goods, real estate, foreclosure assets, and procurement opportunities, then review generated alert candidates with discount and risk notes.

### Deployment Geography for Use:

Global; practical coverage is focused on the listed Chinese-language platforms.

## Known Risks and Mitigations:

Risk: The bundled monitor writes local seen-id and alert history files under the OpenClaw workspace.

Mitigation: Set DEAL_HUNTER_DATA to an approved local directory and define retention expectations before scheduled runs.

Risk: Real scraping, login sessions, Feishu notifications, and cron scheduling are suggested but require operator configuration.

Mitigation: Confirm platform permissions, credential or session handling, recipients, schedule, and alert-data retention before enabling those features.

Risk: The included collectors return simulated example data until real platform integrations are added.

Mitigation: Treat generated alerts as demonstration output unless the collectors have been replaced and validated against approved data sources.

## Reference(s):

- [Valuation Models](artifact/references/valuation-models.md)
- [Risk Signals](artifact/references/risk-signals.md)
- [Platform Rules](artifact/references/platform-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/tujinsama/skills/deal-hunter-alert-claw)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON rule examples, shell commands, and optional JSON alert results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The monitor can write local seen-id and alert log files when executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
