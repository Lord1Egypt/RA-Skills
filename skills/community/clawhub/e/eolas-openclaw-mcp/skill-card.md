## Description:

Trade perpetual futures and send social updates via EOLAS DEX. Place and manage orders on Orderly Network, post updates to Telegram or X/Twitter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albertech2005](https://clawhub.ai/user/albertech2005)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect an OpenClaw agent to EOLAS trading, market-scanning, social posting, and media-generation tools from one agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant live financial and public-account authority through trading, swaps, fund movement, Telegram, X/Twitter, and media-generation tools.

Mitigation: Use only accounts and wallets with limited funds, narrowly scoped and revocable tokens, and enable only the social or media credentials needed for the intended workflow.

Risk: The security summary says strong user controls are not documented for high-impact actions.

Mitigation: Confirm that the gateway enforces approval prompts before placing trades, moving funds, swapping tokens, closing positions, or posting publicly.

Risk: The security guidance notes unpinned packages for the MCP servers.

Mitigation: Prefer pinned package versions or verified releases for the MCP servers before enabling the skill.

## Reference(s):

- [EOLAS MCP on ClawHub](https://clawhub.ai/albertech2005/skills/eolas-openclaw-mcp)
- [EOLAS MCP plugin on npm](https://npmjs.com/package/eolas-openclaw-mcp)
- [EOLAS DEX](https://perps.eolas.fun)
- [EOLAS Docs](https://eolas.gitbook.io/eolas)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown with command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent toward live trading, fund movement, swaps, Telegram messaging, X/Twitter posting, and media generation when the required MCP servers and credentials are configured.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
