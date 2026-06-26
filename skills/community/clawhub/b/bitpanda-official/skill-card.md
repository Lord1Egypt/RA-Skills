## Description: <br>
Queries a Bitpanda account via the Bitpanda API using a bundled bash CLI for read-only balances, portfolio, trade history, transactions, asset info, and live prices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrtlopes](https://clawhub.ai/user/mrtlopes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users with a Bitpanda API key use this skill to retrieve read-only Bitpanda portfolio, balance, price, transaction, and trade information as JSON for account review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a Bitpanda API key and sensitive financial account data. <br>
Mitigation: Use the narrowest read-only API key available and keep BITPANDA_API_KEY out of chat, logs, screenshots, and shell history. <br>
Risk: Outputs can include balances, portfolio holdings, trades, and transaction records. <br>
Mitigation: Review and redact financial outputs before sharing them outside the intended account review workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrtlopes/bitpanda-official) <br>
- [Skill homepage](https://github.com/bitpanda-labs/agent-skills) <br>
- [Bitpanda API Reference](references/api_reference.md) <br>
- [Bitpanda Developer API](https://developer.bitpanda.com) <br>
- [Bitpanda API key setup](https://web.bitpanda.com/my-account/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON from bash CLI commands with brief user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and BITPANDA_API_KEY; uses read-only Bitpanda API endpoints.] <br>

## Skill Version(s): <br>
0.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
