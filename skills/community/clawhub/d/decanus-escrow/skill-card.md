## Description:

Decanus Escrow helps agents create, accept, deliver, complete, dispute, refund, and inspect dual-deposit ETH escrow agreements on Base Sepolia through an MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manueltarouca](https://clawhub.ai/user/manueltarouca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run an MCP escrow server for agent-to-agent task settlement, including escrow creation, seller acceptance, delivery proof submission, release, dispute, refund, and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run unpinned npm code with a wallet private key capable of signing onchain transactions.

Mitigation: Use only a dedicated low-value testnet key, avoid production or reused wallet keys, pin the npm package version when possible, and review before installing.

Risk: Write actions can create, accept, complete, dispute, or refund escrows and may move or lock ETH on Base Sepolia.

Mitigation: Require explicit human review before state-changing escrow transactions and verify addresses, amounts, deadlines, arbiter, and escrow state before signing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/manueltarouca/skills/decanus-escrow)
- [Project Homepage](https://github.com/decanus-labs/escrow-mcp)
- [Base Sepolia RPC](https://sepolia.base.org)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Tool calls]

**Output Format:** [Markdown with inline shell and YAML snippets plus MCP tool parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce state-changing Base Sepolia transaction requests and escrow status summaries.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
