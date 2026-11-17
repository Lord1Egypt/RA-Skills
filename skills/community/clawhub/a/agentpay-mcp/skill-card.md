## Description:

MCP server that gives AI agents the ability to make payments, manage budgets, and handle billing -- directly from Claude Desktop, Cursor, Cline, or any MCP-compatible agent runtime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[up2itnow](https://clawhub.ai/user/up2itnow)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent operators use this MCP server to let compatible agent runtimes send USDC payments, check balances, track spending, manage payment channels, and initiate cross-chain settlement with configured limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-driven crypto payments can cause asset loss if a funded wallet key is exposed, misconfigured, or used beyond intended limits.

Mitigation: Use a dedicated low-balance wallet, avoid primary or treasury keys, keep transaction and daily limits low, and require human approval for larger payments, bridging, or unfamiliar recipients.

Risk: The release asks users to install an unpinned global npm package before granting it access to wallet credentials.

Mitigation: Pin and verify the npm package before installation, run it in an isolated environment, and use a safer secret mechanism where available.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/up2itnow/skills/agentpay-mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP setup instructions and describes payment-related tool calls; runtime behavior depends on configured wallet keys, RPC endpoint, package installation, and spending limits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
