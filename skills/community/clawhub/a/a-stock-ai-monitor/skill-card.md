## Description: <br>
Stock Monitor Pro monitors A-share, ETF, and gold positions with configurable alert rules, optional AI analysis, and trading-signal output for Chinese-investor workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajie1024](https://clawhub.ai/user/ajie1024) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors and developers use this skill to configure watchlists, run market monitoring, and receive alerts, analysis text, and trade-signal guidance for A-share, ETF, and gold holdings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled watchlist can include portfolio details such as symbols, cost basis, and share counts. <br>
Mitigation: Edit or remove the bundled WATCHLIST before running the monitor and avoid storing sensitive portfolio data in shared skill files. <br>
Risk: AI analysis can send portfolio details and alert context to third-party model providers. <br>
Mitigation: Enable AI analysis only after reviewing the provider terms and limiting the data sent in prompts. <br>
Risk: The cron helper can send alerts to a hard-coded Feishu user through a shell command. <br>
Mitigation: Do not run cron_check.py until the Feishu target is replaced and shell=True is removed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ajie1024/a-stock-ai-monitor) <br>
- [Publisher Profile](https://clawhub.ai/user/ajie1024) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [VERSIONS.md](artifact/VERSIONS.md) <br>
- [Moonshot Kimi Chat Completions API](https://api.moonshot.cn/v1/chat/completions) <br>
- [DeepSeek Chat Completions API](https://api.deepseek.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style alert text, JSON trading signals, and shell command/configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use third-party market-data and model APIs; monitoring cadence is described around Beijing market hours.] <br>

## Skill Version(s): <br>
3.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
