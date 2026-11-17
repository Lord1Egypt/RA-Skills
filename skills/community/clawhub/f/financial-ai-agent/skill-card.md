## Description:

Looks up financial market quote data for stocks, ETFs, cryptocurrencies, and indexes when a user provides a symbol or asks about recent prices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iyuanfang](https://clawhub.ai/user/iyuanfang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch market quote data and recent historical prices for common Chinese, Hong Kong, and U.S. securities. It can also help interpret API response metadata such as composite scores and rating levels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A personal Financial Agent API key may be exposed if pasted into a normal chat conversation.

Mitigation: Configure API keys through a dedicated secrets or configuration path when available, and avoid sharing sensitive keys in ordinary prompts.

Risk: The documented OpenClaw configuration update can overwrite existing custom settings in ~/.openclaw/openclaw.json.

Mitigation: Back up or merge the existing configuration before applying the jq update.

Risk: The embedded shared trial API key is visible and has concurrency limits.

Mitigation: Treat the trial key as public, rotate to a personal key for regular use, and monitor API usage.

Risk: The skill makes external market-data API calls as part of normal operation.

Mitigation: Review the target API domain and data handling expectations before using it with sensitive workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iyuanfang/skills/financial-ai-agent)
- [Financial Agent API](https://api.financialagent.cc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API response interpretation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke external HTTPS API calls for market data lookup.]

## Skill Version(s):

1.0.4 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
