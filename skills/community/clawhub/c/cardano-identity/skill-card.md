## Description: <br>
Resolve and list ADAHandles for the connected Cardano wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve ADAHandles owned by a connected Cardano wallet and present those handles as human-readable wallet identifiers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected MCP package requires a wallet seed phrase, which can control the wallet. <br>
Mitigation: Review the package before installation and prefer a low-value isolated wallet or public-address/read-only workflow for handle lookup. <br>
Risk: Installing and running the configured Cardano MCP server may expose sensitive wallet context to third-party code. <br>
Mitigation: Install only from a trusted package source, avoid using a main wallet seed phrase, and verify the MCP server behavior before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adacapo21/cardano-identity) <br>
- [ADAHandle Concepts](references/concepts.md) <br>
- [Identity MCP Tools Reference](references/mcp-tools.md) <br>
- [Resolve ADAHandles](sub-skills/resolve-handles.md) <br>
- [ADAHandle](https://handle.me/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown with ADAHandle strings and wallet-identity guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call MCP wallet tools that depend on SEED_PHRASE configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
