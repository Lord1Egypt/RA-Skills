## Description: <br>
Provides curl-based access to EODHD financial data APIs for company profiles, market prices, fundamentals, economic data, exchange information, and alternative datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mancubus77](https://clawhub.ai/user/mancubus77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route financial-market questions to EODHD REST endpoints and compose curl requests for company profiles, prices, fundamentals, economic indicators, news, options, insider transactions, and exchange data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial research inputs and API credentials are sent to EODHD when requests are executed. <br>
Mitigation: Use a dedicated or limited EODHD API token and keep the token out of chat transcripts, command echoes, and logs. <br>
Risk: EODHD data freshness, rate limits, and costs depend on the account and endpoint used. <br>
Mitigation: Check EODHD rate limits, usage, plan costs, and data freshness before relying on returned market data. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/mancubus77/eodhd-curl) <br>
- [EODHD API base URL](https://eodhd.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and curl commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and an EODHD_API_TOKEN environment variable; responses are requested as JSON when supported.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
