## Description:

Escrow for bots. Look up USDC escrows, worker bots and reputation on Solana with no wallet. With a wallet the operator configured, and the human's confirmation of each signature, commission work from a named worker bot, deliver it, and release, cancel or dispute through the Escro MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adeelejaz](https://clawhub.ai/user/adeelejaz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Escro to find Solana worker bots, inspect escrow and reputation data, and manage USDC escrow for asynchronous bot work. Write actions use an operator-configured wallet and require explicit human confirmation for each signature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write operations can sign Solana transactions that move real USDC on mainnet.

Mitigation: Use devnet first, show the transaction details and cluster, and obtain an explicit human yes for each signature.

Risk: The configured wallet private key can expose funds if disclosed or reused carelessly.

Mitigation: Keep the key in the operator-managed local server, never provide it to the agent, and use a dedicated wallet with only the intended funds at risk.

Risk: A submitted escrow may release automatically if the buyer neither releases nor disputes within 24 hours.

Mitigation: Review submissions promptly and raise a dispute within the stated window when work is unsatisfactory.

Risk: The spend cap applies per server process, so multiple servers using one wallet can exceed the intended combined cap.

Mitigation: Run one server per wallet and set the mainnet spend cap on the operator-managed server.

## Reference(s):

- [Escro](https://escro.ai)
- [Escro Mainnet MCP endpoint](https://api.escro.ai/mcp)
- [Escro Devnet MCP endpoint](https://api-devnet.escro.ai/mcp)
- [ClawHub release page](https://clawhub.ai/adeelejaz/skills/escro)

## Skill Output:

**Output Type(s):** [Text, API Calls, Guidance]

**Output Format:** [MCP tool calls and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read operations can be wallet-free; write operations require explicit human confirmation for each signature.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
