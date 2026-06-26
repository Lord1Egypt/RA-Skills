## Description: <br>
Gate Exchange Assets lets an agent check total assets, account balances, and specific coin holdings across Gate accounts in read-only mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Gate users and their agents use this skill to read and summarize total, per-account, and per-coin balances across configured Gate accounts through a local MCP session. It is intended for asset visibility and account-status questions, not trading or transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads sensitive financial account balances and holdings from the configured Gate MCP session. <br>
Mitigation: Use least-privilege read-only Gate API keys, avoid write permissions, and ask for Gate account data only when that account context is intended. <br>
Risk: Missing MCP configuration, authentication failures, or account-module timeouts can lead to incomplete balance reports. <br>
Mitigation: Keep the Gate MCP session configured with the required read permissions and treat degraded or partial responses as incomplete snapshots. <br>


## Reference(s): <br>
- [Gate Skills Homepage](https://github.com/gate/gate-skills) <br>
- [Gate API Key Management](https://www.gate.com/myaccount/profile/api-key/manage) <br>
- [Gate Exchange Assets Runtime Rules](references/gate-runtime-rules.md) <br>
- [Gate Assets MCP Specification](references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown asset summaries with account distributions and degraded-state notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only responses based on configured Gate MCP account data; no code, files, transfers, or orders are produced.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter lists 2026.4.8-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
