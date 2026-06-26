## Description: <br>
Provides a Python client to query stock positions, account information, orders, deals, watchlists, and market data, and to place or modify orders through Futu OpenAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xdl2003](https://clawhub.ai/user/xdl2003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading automation agents use this skill to connect to a local FutuOpenD instance for brokerage account queries, market data retrieval, and order operations across supported HK, US, and CN markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent access to sensitive brokerage account data. <br>
Mitigation: Keep account data out of chat transcripts and logs, and require explicit approval before retrieving sensitive account details. <br>
Risk: The skill can place, modify, or cancel real brokerage orders. <br>
Mitigation: Keep simulation mode as the default where possible, use least-privilege credentials, and require explicit human approval before any real order operation. <br>


## Reference(s): <br>
- [Futu Client on ClawHub](https://clawhub.ai/xdl2003/futu-client) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Data, Shell commands, Guidance] <br>
**Output Format:** [Python client methods returning pandas DataFrames, dictionaries, booleans, and exceptions; documentation includes Markdown and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FutuOpenD on 127.0.0.1:11111 and the futu-api and pandas Python packages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and artifact/_meta.json, published 2026-03-15) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
