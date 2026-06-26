## Description: <br>
Portfolio news intelligence that monitors breaking news, SEC filings, price moves, and analyst actions for stock, crypto, and ETF holdings, then pushes personalized Telegram alerts with optional AI-powered deep analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdpiano](https://clawhub.ai/user/cdpiano) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this agent to onboard portfolio holdings, receive news and filing alerts through Telegram, update portfolio settings, and request deeper event analysis in the user's selected language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio composition and Telegram delivery credentials are shared with a third-party backend. <br>
Mitigation: Use the skill only when that data sharing is acceptable, create a dedicated Telegram bot token for this service, and revoke the token if the skill is no longer used. <br>
Risk: Secrets such as Telegram and optional Anthropic API keys may be stored locally in plaintext under ~/.firstknow. <br>
Mitigation: Avoid storing high-value API keys unless deep analysis is needed, restrict local machine access, and remove ~/.firstknow when uninstalling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cdpiano/firstknow) <br>
- [Publisher profile](https://clawhub.ai/user/cdpiano) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Chinese README](artifact/README.zh-CN.md) <br>
- [Default configuration](artifact/config/default-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Conversational Markdown with inline shell commands, JSON configuration examples, and portfolio analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May deliver Telegram alerts and deep-analysis messages using user-provided configuration and credentials.] <br>

## Skill Version(s): <br>
0.0.0-git.bdcfd7594c0071040762a54fbbc98ae176330845 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
