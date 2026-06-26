## Description: <br>
Ai News Skills automates an AI-news workflow that collects public web news into Feishu, generates daily reports and morning guides, and synthesizes weekly trend reports with deep dives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yy4fun](https://clawhub.ai/user/yy4fun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators maintaining AI news workflows use this skill suite to collect public AI news, curate high-value daily signals, publish morning briefs, and assemble weekly trend reports in Feishu and OpenClaw-compatible environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled runs can publish reports or guides to configured Feishu destinations. <br>
Mitigation: Configure only intended Feishu tables, wiki spaces, and chat IDs, then perform a manual dry run before enabling cron jobs. <br>
Risk: Source URLs are sent to the Jina Reader URL proxy for public-page extraction. <br>
Mitigation: Use public news sources only and avoid adding private or internal URLs unless sharing those URLs with r.jina.ai is acceptable. <br>
Risk: The installer adds an external Python package and replaces existing ai_news_fetcher and ai_news_reporter directories under the OpenClaw skills folder. <br>
Mitigation: Review install.sh before installation and back up or rename existing local skill directories if they contain changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yy4fun/ai-news-skills) <br>
- [Agent Reach dependency](https://github.com/Panniantong/Agent-Reach) <br>
- [Jina Reader](https://r.jina.ai) <br>
- [Fetcher execution guide](skills/ai_news_fetcher/references/execution.md) <br>
- [Daily reporting guide](skills/ai_news_reporter/references/reporting.md) <br>
- [Weekly reporting guide](skills/ai_weekly_reporter/references/reporting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports and guides, JSON article records, Feishu table/wiki updates, shell commands, and concise execution logs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be written to local report files and configured Feishu tables, wiki spaces, or chats.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata; artifact docs report 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
