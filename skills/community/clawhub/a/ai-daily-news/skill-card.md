## Description: <br>
Automates collection of AI papers, AI products, creator videos, and RSS news items, then generates structured daily reports and pushes them to Feishu. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephleohou-ui](https://clawhub.ai/user/josephleohou-ui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and news workflow maintainers use this skill to configure automated AI news collection, generate daily summaries, schedule runs, and deliver reports to a Feishu chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The YouTube collector can install yt-dlp at runtime if it is missing. <br>
Mitigation: Install reviewed dependencies from artifact/references/requirements.txt in an isolated environment before running the skill, and disable or review runtime package installation paths. <br>
Risk: Browser fallback behavior can invoke broad browser automation commands for scraping. <br>
Mitigation: Run the skill with least privilege, restrict network and browser access where possible, and review configured sources before enabling fallback scraping or scheduled execution. <br>
Risk: Feishu webhook and app credentials in config.json can expose report delivery permissions if shared or committed. <br>
Mitigation: Use a limited Feishu webhook, store config.json outside source control and backups, and rotate credentials if they are exposed. <br>
Risk: Scheduled execution can repeatedly collect and send content without further review. <br>
Mitigation: Enable scheduled runs only after validating source configuration, report contents, and recipient channel behavior with a manual dry run. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/josephleohou-ui/ai-daily-news) <br>
- [Development Guide](artifact/references/DEVELOPMENT.md) <br>
- [Example Configuration](artifact/references/config.example.json) <br>
- [Python Requirements](artifact/references/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON news data, configuration files, logs, and command-oriented guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write config.json, data/daily_news.json, and log files; can send configured reports to a Feishu webhook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
