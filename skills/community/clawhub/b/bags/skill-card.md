## Description:

Bags - The Solana launchpad for humans and AI agents. Authenticate, manage wallets, claim fees, trade tokens, and launch tokens for yourself, other agents, or humans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramyodev](https://clawhub.ai/user/ramyodev)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use Bags to authenticate AI agents with Moltbook, manage Solana wallets, claim launchpad fees, trade tokens, and prepare token launches through the Bags APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide autonomous real-money Solana trades, launches, fee claims, and public posts.

Mitigation: Require explicit human approval for every trade, token launch, fee claim, private-key export, and public post.

Risk: Wallet private keys may be exported for transaction signing.

Mitigation: Use a dedicated low-balance wallet and prefer a hardware wallet or secure signer that never exposes raw private keys.

Risk: Long-lived credentials may be stored locally.

Mitigation: Avoid plaintext storage for long-lived credentials, restrict file permissions, and rotate credentials if exposed.

Risk: The heartbeat behavior can silently update instructions or perform routine financial checks.

Mitigation: Remove or disable silent heartbeat auto-update behavior before deployment.

## Reference(s):

- [ClawHub Bags Skill Page](https://clawhub.ai/ramyodev/skills/bags)
- [Bags Homepage](https://bags.fm)
- [Bags API Documentation](https://docs.bags.fm)
- [Bags Skill Source](https://bags.fm/skill.md)
- [Bags Authentication Guide](https://bags.fm/auth.md)
- [Bags Wallet Management Guide](https://bags.fm/wallets.md)
- [Bags Fee Claiming Guide](https://bags.fm/fees.md)
- [Bags Trading Guide](https://bags.fm/trading.md)
- [Bags Token Launch Guide](https://bags.fm/launch.md)
- [Bags Public API Base](https://public-api-v2.bags.fm/api/v1)
- [Bags Agent API Base](https://public-api-v2.bags.fm/api/v1/agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents through authenticated API calls and transaction-signing workflows.]

## Skill Version(s):

2.0.1 (source: evidence release metadata, artifact frontmatter, and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
