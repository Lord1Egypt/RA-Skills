## Description: <br>
Fortytwo MCP lets an agent query Fortytwo Prime, a paid collective multi-agent inference service, for high-stakes or complex questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[inikitin](https://clawhub.ai/user/inikitin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route explicit or confirmed paid requests to Fortytwo Prime and return the full answer. It also guides wallet setup, preflight checks, session reuse, and troubleshooting for x402 payments using USDC on Base or Monad. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local EVM private key to authorize USDC escrow payments. <br>
Mitigation: Use a dedicated low-value wallet, keep the key in the shell environment rather than chat, avoid shared machines and exposed shell histories, and run preflight before paid calls. <br>
Risk: Paid calls may reserve escrow funds without strong in-code spend controls. <br>
Mitigation: Confirm the selected network and escrow amount before running the query script, and use the service only when the user has explicitly requested or confirmed a paid Fortytwo Prime call. <br>
Risk: A saved billing session can be reused until it expires or the budget is exhausted. <br>
Mitigation: Delete /tmp/.fortytwo_session when finished, use --no-session when a new payment boundary is desired, and include needed context in each query because sessions are billing-only. <br>


## Reference(s): <br>
- [Fortytwo Prime](https://platform.fortytwo.network/prime) <br>
- [ClawHub Skill Page](https://clawhub.ai/inikitin/fortytwo-mcp) <br>
- [Setup & Wallet Configuration](references/setup.md) <br>
- [x402 Payment](references/payment.md) <br>
- [Session Lifecycle](references/session.md) <br>
- [MCP Streaming](references/streaming.md) <br>
- [x402](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text answers with Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the full Fortytwo Prime answer when paid calls succeed; diagnostics are separate from answer text, and follow-up calls may reuse a saved billing session.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
