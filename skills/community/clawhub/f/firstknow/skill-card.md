## Description:

Portfolio news intelligence — monitors breaking news, SEC filings, price moves, and analyst actions for your stock/crypto/ETF holdings. Pushes personalized alerts to Telegram 24/7. Reply "deep" for AI-powered deep analysis. Use when the user wants to set up stock monitoring, check portfolio news, or invokes /firstknow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdpiano](https://clawhub.ai/user/cdpiano)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent to set up portfolio monitoring, receive Telegram alerts for news and market events affecting their holdings, request deeper portfolio-aware analysis, and update holdings or alert settings conversationally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for portfolio holdings, Telegram chat details, and a reusable Telegram bot token.

Mitigation: Use a dedicated Telegram bot, avoid reusing sensitive API keys, and rotate the bot token if you uninstall the skill or suspect exposure.

Risk: The security assessment reports plain local storage and transmission of sensitive data to a custom backend with weak disclosure and controls.

Mitigation: Install only if that data sharing is acceptable, and verify backend deletion and retention behavior before using it for private financial data.

## Reference(s):

- [FirstKnow ClawHub skill page](https://clawhub.ai/cdpiano/skills/firstknow)
- [FirstKnow backend endpoint](https://firstknow-backend.yuchen-9cf.workers.dev)
- [Telegram Bot API endpoint](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational text and Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local FirstKnow configuration and portfolio files and call external backend and Telegram APIs during setup and use.]

## Skill Version(s):

0.0.0-git.bdcfd7594c0071040762a54fbbc98ae176330845 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
