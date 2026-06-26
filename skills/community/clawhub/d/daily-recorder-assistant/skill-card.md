## Description: <br>
每日状态记录与复盘助手。触发词：早反馈/morning query（晨间问询）, 晚复盘/evening review（晚间总结）。支持能量评分、明日规划、当日分析和周期总结。自动识别频道（feishu/telegram/signal/discord），按 User ID 隔离状态数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkctly](https://clawhub.ai/user/tkctly) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and teams use this skill to run structured morning check-ins, evening reviews, daily note capture, next-day planning, and weekly cycle analysis through OpenClaw conversations and optional scheduled reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily records may contain sensitive personal status, planning, or reflection data stored locally in plain text. <br>
Mitigation: Avoid recording sensitive information unless local plain-text storage is acceptable, and keep filesystem access to ~/.openclaw/workspace appropriately restricted. <br>
Risk: Optional scheduled reminders can send prompts to the wrong channel, user, or timezone if cron setup is misconfigured. <br>
Mitigation: Confirm the target channel, user ID, timezone, and existing OpenClaw cron jobs before enabling or re-running setup_cron.py. <br>
Risk: Natural-language trigger inference can misclassify ambiguous check-in or review messages. <br>
Mitigation: Use explicit trigger phrases such as 早反馈, morning query, 晚复盘, or evening review when the message timing or intent is ambiguous. <br>


## Reference(s): <br>
- [Chinese Interaction Templates](references/interaction-templates-zh.md) <br>
- [English Interaction Templates](references/interaction-templates-en-full.md) <br>
- [Daily Recorder Assistant on ClawHub](https://clawhub.ai/tkctly/daily-recorder-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text prompts, Markdown notes and reports, JSON-style state data, and OpenClaw cron configuration commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local daily records under ~/.openclaw/workspace/notes/daily-recorder and may add scheduled OpenClaw reminders when setup_cron.py is run.] <br>

## Skill Version(s): <br>
1.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
