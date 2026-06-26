## Description: <br>
desearch-skill helps agents submit Zeelin Deep Research jobs, monitor them asynchronously, confirm outlines, and save completed research as Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angelandpeiqi](https://clawhub.ai/user/angelandpeiqi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and OpenClaw users use this skill to launch long-running Zeelin research tasks without blocking the active session. It is intended for generating deep research reports from a user-specified topic, thinking mode, and search range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and task content are sent to Zeelin. <br>
Mitigation: Use the skill only for content that is acceptable to process through Zeelin, and avoid submitting confidential or regulated data unless an appropriate agreement and review are in place. <br>
Risk: The Zeelin API key may be stored locally in plaintext. <br>
Mitigation: Prefer environment-based secrets where possible, restrict permissions on local configuration files, and remove the key when the skill is no longer needed. <br>
Risk: The skill can create recurring OpenClaw cron jobs for background checks. <br>
Mitigation: Review active cron jobs after each run and remove the zeelin-check job if a task fails, times out, or is no longer needed. <br>
Risk: Completion details may be sent to a fixed DingTalk recipient without user-scoped control. <br>
Mitigation: Reconfigure or remove the DingTalk recipient before use, and verify notifications are routed only to the intended user or team. <br>
Risk: Packaged report and status files may contain prior research content or session metadata. <br>
Mitigation: Delete bundled report, status, and notification files before installing or redistributing the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/angelandpeiqi/desearch-skill) <br>
- [Publisher profile](https://clawhub.ai/user/angelandpeiqi) <br>
- [Zeelin Deep Research](https://desearch.zeelin.cn) <br>
- [Zeelin API configuration guide](references/config.md) <br>
- [Asynchronous task handling guide](references/async-pattern.md) <br>
- [Installation guide](INSTALL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON status files, and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates saved research reports and status files; may create recurring OpenClaw cron checks while a task is active.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
