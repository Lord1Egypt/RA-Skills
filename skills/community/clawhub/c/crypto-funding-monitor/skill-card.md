## Description:

Monitors RootData and X for crypto funding rounds and token generation events, then sends scheduled or on-demand briefs to Telegram, Discord, or email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhdryanchang](https://clawhub.ai/user/zhdryanchang)

### License/Terms of Use:

MIT

## Use Case:

Developers and crypto analysts use this skill to run a ClawHub-hosted monitoring service for funding and token generation event signals. It supports paid on-demand reports and scheduled notifications across Telegram, Discord, and email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live-looking SkillPay API key is embedded in the artifact.

Mitigation: Treat the key as compromised, rotate it, and replace all documented examples and configuration values with placeholders before use.

Risk: Payment, subscription, and callback controls are exposed without sufficient authentication or webhook verification.

Mitigation: Add authentication and payment webhook verification before enabling paid reports or activating subscriptions.

Risk: Scraped external content is sent through notification channels.

Mitigation: Sanitize scraped fields before generating Telegram, Discord, or email output, and restrict CORS to approved callers.

## Reference(s):

- [Crypto Funding Monitor ClawHub Page](https://clawhub.ai/zhdryanchang/skills/crypto-funding-monitor)
- [Publisher Profile](https://clawhub.ai/user/zhdryanchang)
- [RootData](https://www.rootdata.com)
- [ClawHub Documentation](https://docs.clawhub.com)
- [SkillPay Support](https://skillpay.me/support)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, configuration, shell commands]

**Output Format:** [JSON API responses plus Markdown, Discord embed, and HTML notification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are derived from external crypto funding and TGE data sources and may be sent on demand or by scheduled jobs.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
