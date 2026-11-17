## Description:

Get cryptocurrency token price and generate candlestick charts via CoinGecko API or Hyperliquid API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redf426](https://clawhub.ai/user/redf426)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up cryptocurrency prices, generate candlestick chart images, and summarize recent token movement from CoinGecko or Hyperliquid market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell commands use token symbols and file paths in copy/delete operations, creating command-injection and file-deletion risk.

Mitigation: Validate token symbols, generate safe filenames, and perform copy/delete operations through structured APIs or quoted argument arrays.

Risk: Installing or running the skill before remediation may expose the workspace to unsafe cleanup behavior.

Mitigation: Review before installation and run only in a sandboxed environment until the command-handling issues are fixed.

## Reference(s):

- [ClawHub Crypto Chart skill page](https://clawhub.ai/redf426/skills/crypto-chart)
- [Hyperliquid API endpoint](https://api.hyperliquid.xyz/info)
- [CoinGecko API](https://api.coingecko.com/api/v3/)

## Skill Output:

**Output Type(s):** [text, JSON, image files, shell commands]

**Output Format:** [JSON with text fields and an optional PNG chart path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create temporary PNG chart files and cached price JSON files under /tmp.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
