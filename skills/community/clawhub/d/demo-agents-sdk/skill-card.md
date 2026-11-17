## Description:

Polygon Agent Kit helps agents create session-based smart contract wallets, perform token operations, register ERC-8004 identities, and make x402 micropayments through a single CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameslawton](https://clawhub.ai/user/jameslawton)

### License/Terms of Use:


## Use Case:

Developers and autonomous-agent builders use this skill to set up Polygon smart contract wallets, configure session permissions, fund wallets, register on-chain agent identity, and perform token operations from a CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles crypto wallet sessions and token operations.

Mitigation: Use a dedicated low-privilege environment and a limited wallet, and review commands before broadcasting transactions.

Risk: The workflow may install or use cloudflared and expose a temporary approval callback through a tunnel.

Mitigation: Pin and verify packages and the cloudflared binary, and prefer explicit or manual modes when tunnel behavior is not acceptable.

Risk: Approval URLs and session ciphertext can grant access if shared or retained carelessly.

Mitigation: Share approval URLs only within the active approval flow, never reuse old approval URLs, and clean up session ciphertext written under /tmp.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jameslawton/skills/demo-agents-sdk)
- [Polygon Agent Kit repository](https://github.com/0xPolygon/polygon-agent-kit)
- [Sequence ecosystem connector](https://agentconnect.staging.polygon.technology/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes wallet approval URLs, environment variables, CLI flags, and troubleshooting steps.]

## Skill Version(s):

0.1.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
