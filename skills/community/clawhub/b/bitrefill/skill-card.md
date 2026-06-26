## Description: <br>
Bitrefill routes agents to browse or purchase Bitrefill gift cards, mobile top-ups, and eSIMs through the highest-fidelity available channel: residential browser, MCP server, npm CLI, or REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcopesani](https://clawhub.ai/user/marcopesani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help an agent find, compare, and, with explicit approval, buy Bitrefill digital goods such as gift cards, mobile top-ups, and eSIMs. <br>

### Deployment Geography for Use: <br>
Global, subject to Bitrefill product availability, payment support, and regional checkout restrictions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent real purchase authority for instantly delivered digital goods. <br>
Mitigation: Require explicit confirmation before purchase, keep buy tools out of auto-approval, and use a dedicated low-balance Bitrefill account. <br>
Risk: The skill may use OAuth tokens, API keys, credential files, or environment variables. <br>
Mitigation: Prefer OAuth or Authorization-header setup over keys in URLs, protect local credential files, and do not commit secrets or plaintext keys. <br>
Risk: Gift card codes, eSIM QR codes, and redemption links are cash-like once delivered. <br>
Mitigation: Handle redemption details in memory when possible, avoid public or shared channels, avoid plaintext logs, and advise prompt redemption. <br>
Risk: Crypto or x402 payment flows can spend from agent-accessible funds. <br>
Mitigation: Never provide wallet seed phrases or signing keys to the agent, and bound available balances before enabling autonomous payment flows. <br>


## Reference(s): <br>
- [Skill README](SKILL.md) <br>
- [Bitrefill Website](https://www.bitrefill.com) <br>
- [Bitrefill Documentation](https://docs.bitrefill.com) <br>
- [Bitrefill CLI Repository](https://github.com/bitrefill/cli) <br>
- [MCP Path](references/mcp.md) <br>
- [CLI Path](references/cli.md) <br>
- [REST API Path](references/api.md) <br>
- [Browse Path](references/browse.md) <br>
- [Spending Safeguards](references/safeguards.md) <br>
- [Capability Matrix](references/capability-matrix.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline command, JSON, and HTTP examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP setup, CLI commands, REST calls, purchase confirmations, invoice IDs, and redemption-handling guidance.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release metadata; artifact frontmatter lists 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
