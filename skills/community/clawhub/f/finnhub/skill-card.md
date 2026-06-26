## Description: <br>
Access Finnhub API for real-time stock quotes, company news, market data, financial statements, and trading signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthewxfz3](https://clawhub.ai/user/matthewxfz3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to configure Finnhub API access and compose requests for quotes, company news, market data, financial statements, earnings data, SEC filing search, and trading indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Finnhub API key, and exposed tokens or unmonitored use can create account, quota, or cost risk. <br>
Mitigation: Use an appropriately scoped key, store it in environment configuration, monitor usage and costs, and avoid sharing logs or URLs that include the token. <br>
Risk: Some Finnhub endpoints, market data, or trading indicators may be tier-limited, rate-limited, delayed, or unavailable for a given account. <br>
Mitigation: Check the Finnhub plan and endpoint availability before relying on responses, and treat market data or signals as inputs for review rather than final trading instructions. <br>


## Reference(s): <br>
- [Finnhub](https://finnhub.io) <br>
- [Finnhub API base URL](https://finnhub.io/api/v1) <br>
- [ClawHub Finnhub skill release](https://clawhub.ai/matthewxfz3/finnhub) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a FINNHUB_API_KEY for Finnhub requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
