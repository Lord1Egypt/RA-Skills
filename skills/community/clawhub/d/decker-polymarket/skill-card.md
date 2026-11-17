## Description:

Use when the user asks an agent to search Polymarket prediction markets through Decker, inspect categories, events, market slugs, prices, positions, or prepare YES/NO order requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gigshow](https://clawhub.ai/user/gigshow)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to work with Polymarket prediction markets via Decker, including market discovery, market detail lookup, YES/NO order-request preparation, and position checks where credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet private key exposure can give Decker or anyone with access to the key control over funds associated with that wallet.

Mitigation: Use a dedicated low-balance Polygon wallet, do not reuse a wallet that holds other assets, and prefer wallet-native signing or scoped revocable credentials when available.

Risk: Authentication secrets in request URLs may be logged or replayed for financially consequential requests.

Mitigation: Require explicit confirmation before trade requests, avoid sharing or storing request URLs, and rotate any exposed secret.

## Reference(s):

- [Decker API](https://api.decker-ai.com)
- [Polymarket](https://polymarket.com)
- [ClawHub skill page](https://clawhub.ai/gigshow/skills/decker-polymarket)
- [Publisher profile](https://clawhub.ai/user/gigshow)

## Skill Output:

**Output Type(s):** [guidance, API Calls, configuration, shell commands]

**Output Format:** [Markdown with inline URL and request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include financially consequential trade-request guidance that should be reviewed before execution.]

## Skill Version(s):

1.1.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
