## Description: <br>
A股智投大师 helps agents analyze A-share market data, fundamentals, stock screening, watchlists, news, and monitoring alerts using East Money/Miaoxiang-dependent skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasxing1](https://clawhub.ai/user/lucasxing1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query A-share prices, review fundamentals and news, screen stocks, manage watchlists, and set monitoring alerts for investment research. Outputs are informational and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad prompts can add or delete remote self-selected stocks or create monitoring alerts. <br>
Mitigation: Require explicit user confirmation before watchlist changes or alert creation, and show the exact stock and rule before execution. <br>
Risk: The skill depends on external financial-data skills and an East Money/Miaoxiang API key. <br>
Mitigation: Review dependent skills before installation and configure the API key only when the East Money/Miaoxiang service is trusted. <br>
Risk: Financial analysis and market data may be delayed, incomplete, or unsuitable for trading decisions. <br>
Mitigation: Present outputs as informational research, preserve the investment-risk disclaimer, and prompt users to verify data before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucasxing1/a-stock) <br>
- [Publisher profile](https://clawhub.ai/user/lucasxing1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands and JSON-like data summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an East Money/Miaoxiang API key and dependent OpenClaw skills.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
