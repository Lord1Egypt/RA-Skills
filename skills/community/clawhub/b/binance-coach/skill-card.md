## Description: <br>
Binance Coach helps Binance users analyze read-only portfolio data, review trading behavior, get DCA and market-context guidance, configure alerts, follow Binance announcements, and request AI coaching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[UnrealBNB](https://clawhub.ai/user/UnrealBNB) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Binance users use this skill through an agent to inspect portfolio health, market indicators, behavioral trading patterns, DCA recommendations, alerts, and crypto education. Users can optionally run Telegram or AI-coaching modes that share selected financial context with external services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Binance portfolio data, trade history, and API credentials. <br>
Mitigation: Use read-only Binance API keys, restrict keys by IP where possible, keep secrets local, and avoid logging credentials in agent conversations or terminal output. <br>
Risk: Optional Anthropic and Telegram modes can share financial context with external services. <br>
Mitigation: Enable those modes only when external processing and Telegram delivery are acceptable for the user's financial context. <br>
Risk: Optional default-handler hooks, crons, Telegram polling, and announcement watchers can create persistent or recurring crypto-related flows. <br>
Mitigation: Decline the USER.md hook, scheduled crons, and background watchers unless persistent routing or recurring reports are intentionally desired. <br>
Risk: The server security verdict is suspicious because the release combines real portfolio coaching with sensitive data handling and optional persistent integrations. <br>
Mitigation: Review the bundled source, setup behavior, and generated local files before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/UnrealBNB/binance-coach) <br>
- [BinanceCoachAI Homepage](https://github.com/UnrealBNB/BinanceCoachAI) <br>
- [Security and Privacy](SECURITY.md) <br>
- [Agent Guide](references/agent-guide.md) <br>
- [Command Reference](references/commands.md) <br>
- [Setup Guide](references/setup.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with command examples and optional local configuration files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local .env and SQLite data files during setup or runtime; optional Telegram and scheduled-analysis modes can emit recurring notifications.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
