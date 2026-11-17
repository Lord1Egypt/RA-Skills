## Description:

DashPass is an encrypted credential vault on Dash Platform that lets AI agents store, retrieve, rotate, and export API keys, tokens, and passwords.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dashbot-0001](https://clawhub.ai/user/dashbot-0001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use DashPass to manage agent-accessible credentials on Dash Platform, including storing, retrieving, rotating, listing, checking expiry, and exporting secrets through a Node.js CLI. Use testnet or low-impact secrets unless the approval and audit controls described in the security evidence are addressed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents with the vault environment may be able to read, export, rotate, or delete critical secrets without the promised human approval.

Mitigation: Limit the vault environment to trusted agents, use testnet or low-impact secrets, and add an external approval gate before storing critical credentials.

Risk: Environment export flows can expose sensitive secrets when used with shell evaluation.

Mitigation: Avoid eval-based export for sensitive credentials; prefer narrowly scoped process injection and short-lived environment variables.

Risk: CRITICAL_WIF and the recovery mnemonic grant full vault control if exposed.

Mitigation: Keep both out of chats, logs, shell history, repositories, and synced folders; store recovery words offline and rotate or revoke access after exposure.

Risk: Local cache behavior may retain credential data on disk for fast access.

Mitigation: Disable caching with DASHPASS_CACHE=none when operating on sensitive secrets or on shared machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dashbot-0001/skills/dashpass)
- [DashPass CLI Command Reference](references/cli-commands.md)
- [DashPass Security Model](references/security-model.md)
- [DashPass Trust Architecture](references/trust-architecture.md)
- [DashPass Security Analysis Summary](references/security-analysis-summary.md)
- [DashPass FAQ and Known Limitations](references/faq.md)
- [First-Time Setup](setup.md)
- [Dash Platform Identity tutorial](https://docs.dash.org/en/stable/docs/tutorials/identities-and-names.html)
- [Dash Platform identity top-up tutorial](https://docs.dash.org/en/stable/docs/tutorials/identities-and-names.html#top-up-an-identity)
- [Dash testnet faucet](https://testnet-faucet.dash.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces CLI command guidance for Node.js-based credential operations and recovery workflows.]

## Skill Version(s):

0.9.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
