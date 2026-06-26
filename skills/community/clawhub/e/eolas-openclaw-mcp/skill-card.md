## Description: <br>
Trade perpetual futures and send social updates via EOLAS DEX. Place and manage orders on Orderly Network, post updates to Telegram or X/Twitter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albertech2005](https://clawhub.ai/user/albertech2005) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to connect an agent to EOLAS trading, market-scanning, wallet, Telegram, X/Twitter, and media-generation tools from a conversational workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured agents can place trades, manage funds, swap tokens, close positions, and publish public messages. <br>
Mitigation: Require explicit user approval for every trade, withdrawal, swap, position close, and public post. <br>
Risk: Wallet credentials and social or media API tokens can expose funds or public accounts if over-privileged or misused. <br>
Mitigation: Use a dedicated low-balance wallet, separate social accounts, least-privileged API tokens, and disable the plugin when it is not actively needed. <br>
Risk: The security verdict is suspicious because the release grants real-funds and public-account authority without clear built-in limits. <br>
Mitigation: Review the npm packages and source before installing, then apply local policy controls around high-impact actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/albertech2005/eolas-openclaw-mcp) <br>
- [EOLAS Docs](https://eolas.gitbook.io/eolas) <br>
- [EOLAS DEX](https://perps.eolas.fun) <br>
- [npm Package](https://npmjs.com/package/eolas-openclaw-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown and conversational text with inline shell commands, JSON configuration, and tool-directed actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger external trading, wallet, messaging, social-posting, and media-generation actions when the plugin is enabled and configured.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
