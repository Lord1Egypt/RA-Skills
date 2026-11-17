## Description:

Helps agents discover AI agents and x402 tools, sign in with a Solana wallet, and prepare user-approved token launches, trades, and fee claims through Deside.

This skill is ready for commercial/non-commercial use.

## Publisher:

[desideapp](https://clawhub.ai/user/desideapp)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use Deside to find agents and x402 tools with reported check status, authenticate with a Solana wallet, and prepare token launches, trades, and fee claims for user approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet files, signatures, and OAuth tokens may expose account access if mishandled.

Mitigation: Keep wallet secrets local; confirm the host, network, and signed message or transaction before authorizing it.

Risk: Mainnet launches, trades, and x402 calls can spend funds.

Mitigation: Show the cost and transaction details and obtain user approval before signing or paying; rehearse launches and trades on devnet.

Risk: Third-party x402 tools may receive private prompts or secrets.

Mitigation: Review the destination and avoid sending sensitive information to tools found through the directory.

Risk: Directory checks may be stale or mistaken for a safety endorsement.

Mitigation: Report the precise state and check date; do not equate a live endpoint or listing with quality or safety.

## Reference(s):

- [Deside skill release](https://clawhub.ai/desideapp/skills/deside)
- [Directory API](https://deside.io/skill/directory-api.md)
- [Ask and x402 payments](https://deside.io/skill/ask.md)
- [MCP tools](https://deside.io/skill/mcp-tools.md)
- [Wallet and sign-in](https://deside.io/skill/wallet-and-signin.md)
- [Launchpad](https://deside.io/skill/launchpad.md)
- [Errors and limits](https://deside.io/skill/errors-and-limits.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with API examples and transaction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Distinguishes reported directory states from endorsements; financial actions require user approval and wallet signing.]

## Skill Version(s):

1.0.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
