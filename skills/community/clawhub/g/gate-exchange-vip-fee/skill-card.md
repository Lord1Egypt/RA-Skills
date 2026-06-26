## Description: <br>
Gate VIP tier and trading fee query skill for checking a user's Gate VIP level and trading fee rates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate users use this skill to query their current VIP tier and spot or futures maker/taker fee rates through read-only Gate MCP account and wallet tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill delegates mandatory runtime behavior to an unpinned remote GitHub rules file. <br>
Mitigation: Review the remote runtime rules before installation or execution, and pin or vendor a reviewed copy where deployment policy requires immutable instructions. <br>
Risk: The skill accesses user-specific Gate account and wallet fee data through authenticated MCP tools. <br>
Mitigation: Use only Gate OAuth or read-only Gate API keys with Account:Read and Wallet:Read permissions; do not grant trading or withdrawal permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-exchange-vip-fee) <br>
- [Gate publisher profile](https://clawhub.ai/user/gate-exchange) <br>
- [MCP execution specification](references/mcp.md) <br>
- [Usage scenarios](references/scenarios.md) <br>
- [Gate MCP](https://github.com/gateio/gate-mcp) <br>
- [Gate API key management](https://www.gate.io/myaccount/profile/api-key/manage) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown tables and structured summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports only queried VIP and fee fields, keeps values as returned by the API, and includes scope notes when pair-specific fee requests may still return account-level fees.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
