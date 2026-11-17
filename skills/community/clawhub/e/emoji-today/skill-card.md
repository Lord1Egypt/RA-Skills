## Description:

Vote in the daily emoji election on emoji.today.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bill-makes](https://clawhub.ai/user/bill-makes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use the skill to cast a daily emoji vote associated with a Farcaster ID; they can optionally mint the vote as an NFT.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to publish about votes on X and Farcaster without a separate opt-in.

Mitigation: Require explicit approval before any public post.

Risk: Voting and optional minting spend USDC through the configured wallet.

Mitigation: Use a dedicated wallet with a small balance, protect its private key, and review the $0.01 vote and optional $1 mint charges.

Risk: The supplied security guidance identifies a Zod advisory affecting the current dependency set.

Mitigation: Request a compatible dependency update that addresses the advisory.

## Reference(s):

- [emoji.today](https://emoji.today)
- [Neynar (Farcaster ID lookup)](https://neynar.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, JSON]

**Output Format:** [Markdown instructions, shell commands, and JSON response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Farcaster ID and an EVM wallet; voting and optional NFT minting use Base USDC payments.]

## Skill Version(s):

1.2.1 (source: frontmatter, scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
