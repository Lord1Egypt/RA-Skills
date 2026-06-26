## Description: <br>
人格修行系统 helps an agent generate scheduled morning wisdom prompts, evening reflection prompts, virtue rotation reminders, quote-library guidance, and optional journal archive instructions for a daily cultivation workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opc8838-hub](https://clawhub.ai/user/opc8838-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to configure a daily personal reflection system that sends morning wisdom, evening review prompts, and weekly virtue reminders through selected channels. The workflow can save evening reflections to a private local vault for later search and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evening reflections may contain private personal information saved in the configured vault. <br>
Mitigation: Use a private local vault, verify the save path before enabling auto-save, and disable auto-save when a local-only unsaved workflow is preferred. <br>
Risk: Reminder content may be sent to unintended people if channel targets or group chats are misconfigured. <br>
Mitigation: Verify channel target, timezone, and cron entries before deployment, and avoid group chats for sensitive reflections. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/opc8838-hub/daily-cultivation) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [Configuration guide](references/config-guide.md) <br>
- [Franklin virtues reference](references/franklin-virtues.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include scheduled reminder content, reflection templates, channel configuration, and local archive paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
