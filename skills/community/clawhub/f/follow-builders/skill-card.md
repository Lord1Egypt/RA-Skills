## Description: <br>
AI builders digest that monitors top AI builders on X and YouTube podcasts and remixes their content into digestible summaries for AI industry insights, builder updates, or /ai requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zarazhangrui](https://clawhub.ai/user/zarazhangrui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a daily or weekly AI builder digest from curated X accounts and YouTube podcasts, then receive concise summaries in chat, Telegram, email, or terminal output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch current prompt instructions and feeds from remote sources. <br>
Mitigation: Review the prepared digest content before delivery, and use local prompt overrides when you need stable summarization behavior. <br>
Risk: Telegram or email delivery can store third-party delivery credentials locally. <br>
Mitigation: Use stdout or on-demand delivery when possible, and only add Telegram or Resend credentials when off-terminal delivery is required. <br>
Risk: Automatic delivery can create recurring scheduled jobs. <br>
Mitigation: Inspect any OpenClaw cron or system crontab entry after setup and remove scheduled delivery if it is not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zarazhangrui/follow-builders) <br>
- [README](artifact/README.md) <br>
- [Configuration Schema](artifact/config/config-schema.json) <br>
- [Default Sources](artifact/config/default-sources.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest text with setup guidance, shell command snippets, and JSON-backed configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local settings under ~/.follow-builders and configure recurring delivery jobs when automatic delivery is enabled.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
