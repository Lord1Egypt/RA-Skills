## Description: <br>
Binance Square (币安广场) signal agent that scrapes public Binance Square posts with Puppeteer/API interception, detects bot-pushed crypto narratives, optionally checks Coinglass on-chain indicators, and produces LONG, SHORT, AVOID, or WATCH trading research outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ru7superbeauty](https://clawhub.ai/user/ru7superbeauty) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan Binance Square narratives, identify likely bot amplification, cross-check optional on-chain indicators, and generate crypto market research reports. The outputs are research signals and are not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scrapes public Binance Square pages and stores scan results and reports locally. <br>
Mitigation: Run it only where local storage of the scraped dataset and generated reports is acceptable, and review saved files before sharing them. <br>
Risk: Telegram delivery can expose generated signal summaries to a configured chat. <br>
Mitigation: Use a dedicated Telegram bot token and chat ID, and review message text before invoking the Telegram push mode. <br>
Risk: Directional outputs can be mistaken for financial advice. <br>
Mitigation: Treat outputs as crypto research signals only and apply independent trading, compliance, and risk review before acting on them. <br>
Risk: On-chain confirmation depends on a user-supplied Coinglass API or proxy base URL. <br>
Mitigation: Use a trusted Coinglass endpoint or proxy and expect degraded direction calls when COINGLASS_BASE is not configured. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ru7superbeauty/binance-square-skill) <br>
- [Binance market coin information](https://www.binance.com/zh-CN/markets/coinInfo) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>
- [Telegram user info bot](https://t.me/userinfobot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, saved Markdown reports, local JSON scrape data, and optional Telegram message text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces directional crypto research signals and local report files; optional Telegram delivery requires user-provided Telegram credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
