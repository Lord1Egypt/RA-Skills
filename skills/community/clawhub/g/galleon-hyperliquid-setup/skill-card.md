## Description:

Connects an agent's available tools to Hyperliquid workflows and verifies a first public market read without granting trading authority.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galleonlabs](https://clawhub.ai/user/galleonlabs)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to check available Hyperliquid tools, obtain a timestamped public market snapshot, and identify which analysis or account workflows are ready and which require separate access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public market read could be mistaken for account access or trading authorization.

Mitigation: Treat setup as read-only; require a public account address for account reads and a separately trusted signer with explicit approval for execution. Never provide private keys.

Risk: An optional skill installation command could add unreviewed capabilities.

Mitigation: Treat any optional `npx skills add` command as a separate installation decision; do not install tools or grant wallet authority automatically.

## Reference(s):

- [Connections and first run](references/connections.md)
- [Agent integration and handoffs](references/agent-integration.md)
- [Official Hyperliquid tools](references/official-tools.md)
- [Hyperliquid API documentation](https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown readiness report; JSON public market snapshot when the helper is used]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes network, market, observation time, prices, spread, funding, data gaps, and next action; a public read does not establish account or trading access.]

## Skill Version(s):

0.4.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
