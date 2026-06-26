## Description: <br>
AI-assisted daily diary system that reviews the day's conversations, extracts key events, decisions, and insights, and generates a structured diary draft for user review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyu925065781](https://clawhub.ai/user/luyu925065781) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals who want a daily journal use this skill to turn the day's conversations into a structured diary draft, add reflections or mood notes, and archive the result locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill summarizes private conversation history into diary content. <br>
Mitigation: Review diary drafts before relying on them, keep diary files private, and redact or omit sensitive information. <br>
Risk: Automated scheduling or delivery can expose diary drafts if the timezone, channel, or recipient is configured incorrectly. <br>
Mitigation: Set the timezone and delivery target deliberately, and deliver drafts only to the conversation owner or a private channel. <br>
Risk: The workflow may save an unreviewed draft after 24 hours. <br>
Mitigation: Adjust or disable the timeout behavior when explicit confirmation is required before storing diary files. <br>


## Reference(s): <br>
- [Daily Diary on ClawHub](https://clawhub.ai/luyu925065781/daily-diary) <br>
- [Diary Template](assets/diary-template.md) <br>
- [Guided Prompts for Diary Entries](references/quick-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diary drafts, local Markdown diary files, and optional JSON cron configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Designed to save diary entries under ~/diary/ and deliver drafts only through the user's configured private channel.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
