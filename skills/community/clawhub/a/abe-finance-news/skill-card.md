## Description: <br>
Market news briefings with AI summaries for stock news, market updates, portfolio performance, morning or evening briefings, financial headlines, and price alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to generate market briefings, portfolio news summaries, stock-specific updates, and price or earnings alerts across US, European, and Japanese markets. It supports English or German output and optional WhatsApp or Telegram delivery through OpenClaw and Lobster workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cron scripts may send portfolio-related briefings or alerts to a hardcoded default WhatsApp target if the destination is not reviewed. <br>
Mitigation: Review and set FINANCE_NEWS_TARGET before enabling cron scripts or automated delivery. <br>
Risk: The skill stores local portfolio or alert data and may call finance, news, AI, OpenBB, OpenClaw, or Gemini-related tooling. <br>
Mitigation: Install and run it only in an environment where those local data stores, credentials, services, and tools are approved. <br>


## Reference(s): <br>
- [Skill README](README.md) <br>
- [Premium Source Authentication](docs/PREMIUM_SOURCES.md) <br>
- [Lobster Workflows](workflows/README.md) <br>
- [OpenClaw Lobster](https://github.com/openclaw/lobster) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings, JSON output, and CLI or workflow command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefings can be generated in English or German and may be sent through configured WhatsApp or Telegram targets.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
