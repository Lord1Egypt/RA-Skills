## Description: <br>
Market news briefings with AI summaries. Use when asked about stock news, market updates, portfolio performance, morning/evening briefings, financial headlines, or price alerts. Supports US/Europe/Japan markets, WhatsApp delivery, and English/German output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate market news briefings, portfolio-focused updates, stock headlines, earnings and alert checks, and scheduled WhatsApp or Telegram delivery in English or German. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated cron scripts may send portfolio, alert, or earnings information to a hard-coded WhatsApp recipient if run unchanged. <br>
Mitigation: Review cron scripts before installation, remove the default FINANCE_NEWS_TARGET value, and explicitly set the intended delivery target and channel. <br>
Risk: No-approval scheduled workflows can distribute financial briefing content without a final human check. <br>
Mitigation: Prefer workflows with approval gates until the configured sources, targets, language, and schedule have been reviewed. <br>
Risk: Debug output, raw JSON, portfolio files, and API keys may contain sensitive financial data. <br>
Mitigation: Treat generated files and logs as sensitive, restrict access to configuration and portfolio files, and avoid sharing raw outputs publicly. <br>


## Reference(s): <br>
- [Finance News Litiao on ClawHub](https://clawhub.ai/litiao1224/finance-news-litiao) <br>
- [README](artifact/README.md) <br>
- [Premium Source Authentication](artifact/docs/PREMIUM_SOURCES.md) <br>
- [Workflow Documentation](artifact/workflows/README.md) <br>
- [Lobster Workflow Engine](https://github.com/openclaw/lobster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings and optional JSON output with shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can generate scheduled morning/evening briefings, portfolio updates, price alerts, earnings summaries, and delivery workflow outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
