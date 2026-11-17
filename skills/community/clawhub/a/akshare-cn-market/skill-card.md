## Description:

Provides Chinese A-share market, index, financial-summary, macroeconomic, bond-yield, and trading-calendar data through AKShare-backed Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geoion](https://clawhub.ai/user/geoion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis agents use this skill to retrieve Chinese A-share historical prices, index data, company financial summaries, macroeconomic indicators, bond yields, and A-share trading-calendar information. Outputs are research data and should not be used as standalone investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AKShare contacts public finance data providers, so use may disclose requests to external services and depend on their availability.

Mitigation: Run the skill only in an approved network environment and handle provider timeouts or missing fields in agent workflows.

Risk: Installing unpinned dependencies can resolve newer AKShare or pandas versions than the release was written against.

Mitigation: Use a virtual environment, avoid elevated privileges, and pin reviewed dependency versions before deployment.

Risk: Market and macroeconomic outputs can be delayed, incomplete, or unsuitable for direct investment decisions.

Mitigation: Treat the data as research input, verify important values against authoritative sources, and require human review for investment decisions.

Risk: Some real-time or push-style endpoints may fail in proxied or sandboxed environments.

Mitigation: Prefer the documented stable historical, Sina index, macroeconomic, and calendar endpoints, and include fallback behavior for blocked endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geoion/skills/akshare-cn-market)
- [AKShare reference README](references/README.md)
- [AKShare official documentation](https://akshare.akfamily.xyz/)
- [AKShare GitHub repository](https://github.com/akfamily/akshare)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing Python script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included scripts print JSON arrays or error objects for market, macroeconomic, bond-yield, and trading-calendar requests.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
