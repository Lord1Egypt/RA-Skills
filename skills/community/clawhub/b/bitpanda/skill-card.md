## Description: <br>
Check a Bitpanda crypto portfolio, wallet balances, trade history, and asset prices from the command line using a local API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[florianbeer](https://clawhub.ai/user/florianbeer) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to inspect Bitpanda holdings, non-zero wallet balances, recent buy/sell trades, and asset prices without initiating trades or transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve and display Bitpanda balances, wallet IDs, and trade history. <br>
Mitigation: Use a dedicated least-privilege API key and run the skill only where that account information may be shown. <br>
Risk: A stored API key could be exposed if the local credentials file is readable by other users or tools. <br>
Mitigation: Protect the credentials file with restrictive permissions and revoke the key when it is no longer needed. <br>
Risk: Overbroad API-key scopes could increase account exposure beyond read-only viewing. <br>
Mitigation: Avoid withdrawal or trading permissions and grant only the read scopes needed for balances, trades, and transactions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/florianbeer/bitpanda) <br>
- [Publisher Profile](https://clawhub.ai/user/florianbeer) <br>
- [Bitpanda API Key Settings](https://web.bitpanda.com/my-account/apikey) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Configuration instructions, Guidance] <br>
**Output Format:** [Terminal text and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, bc, and a Bitpanda API key supplied through an environment variable or local credentials file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
