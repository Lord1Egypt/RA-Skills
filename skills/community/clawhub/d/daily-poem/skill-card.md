## Description: <br>
Daily Poem helps agents deliver daily and on-demand poems in Chinese or English with translation, background, analysis, and recitation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to receive a morning poem, request poems by mood, season, theme, author, or form, and receive a weekly poetry digest. It is useful for poetry discovery, bilingual appreciation, and lightweight literary analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional scheduled poem reminders can continue running after installation if the user enables the documented cron commands. <br>
Mitigation: Review the cron commands before enabling scheduled pushes, and use cron list/delete or the documented push-toggle guidance to turn reminders off. <br>
Risk: Generated poem analysis and translations may be subjective or imperfect. <br>
Mitigation: Treat commentary as literary guidance and review important translations, interpretations, and source selections before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cosmofang/daily-poem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style text with poem prompts, translations, analysis notes, and cron setup commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce scheduled reminder prompts when the user enables OpenClaw cron commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
