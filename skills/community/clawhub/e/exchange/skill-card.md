## Description:

Provides exchange-rate conversion, currency lists, bank foreign-exchange rates, realtime quote data, and historical exchange-rate queries through JisuAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer currency conversion, bank foreign-exchange quote, realtime market quote, and historical exchange-rate questions. Developers can call the included Python script with JSON or subcommands after configuring a JisuAPI AppKey.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Currency query details and the JisuAPI AppKey are sent to JisuAPI endpoints.

Mitigation: Use a service-scoped AppKey, avoid unnecessary personal or account information in queries, and monitor quota or billing usage.

Risk: Exchange-rate data is reference information and may not be suitable as the sole basis for financial decisions.

Mitigation: Verify important rates with the relevant bank, exchange, or authoritative source before acting on them.

## Reference(s):

- [JisuAPI Exchange Rate API Documentation](https://www.jisuapi.com/api/exchange/)
- [JisuAPI](https://www.jisuapi.com/)
- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/exchange)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jisuapi)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JISU_API_KEY; API results can include exchange-rate data, realtime quotes, historical records, or structured error objects.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
