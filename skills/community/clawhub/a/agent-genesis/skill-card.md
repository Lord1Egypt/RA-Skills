## Description:

Agent Genesis allows Agents to mine Agent Genesis Coin (AGC) and use it as native working capital. Earn AGC through Proof of Agent (POA).

This skill is ready for commercial/non-commercial use.

## Publisher:

[likwid-tech](https://clawhub.ai/user/likwid-tech)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to bootstrap a wallet, mine Agent Genesis Coin through Proof of Agent workflows, and manage AGC through Likwid DeFi actions such as swaps, liquidity, margin, and claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote installers and dependencies can change between review and execution.

Mitigation: Review and pin the bootstrap script and dependency versions before installation or update.

Risk: The skill can operate real blockchain wallets and DeFi transactions.

Mitigation: Use a disposable low-value wallet and require explicit human approval for each transaction, approval, EIP-7702 delegation, margin action, or live-chain test.

Risk: Private keys and MODEL_KEY values are handled through local plaintext files.

Mitigation: Treat wallet files and .env values as secrets, never paste private keys into chat, and restrict local file access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/likwid-tech/skills/agent-genesis)
- [Agent Genesis Whitepaper](https://raw.githubusercontent.com/likwid-fi/agent-genesis/refs/heads/main/agc_whitepaper_en.md)
- [Likwid.fi](https://likwid.fi)
- [README](README.md)
- [Security Audit](audit/AGC_SECURITY_AUDIT_v3.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command blocks and CLI arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit human review for wallet creation, secrets, signatures, transactions, approvals, and DeFi actions.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
