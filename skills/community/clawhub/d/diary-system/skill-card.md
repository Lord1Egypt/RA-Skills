## Description: <br>
Configure an AI diary system for OpenClaw that helps users enable, set up, or share diary behavior for an agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adolescen-he](https://clawhub.ai/user/adolescen-he) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure an agent diary feature, including setup guidance, diary templates, and state tracking for whether the latest diary has been read. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause persistent diary files to store private diary content and observations about the user. <br>
Mitigation: Require explicit consent before enabling diary writes, review the diary directory regularly, and avoid recording sensitive personal information. <br>
Risk: The skill modifies SOUL.md, USER.md, and AGENTS.md and changes session startup behavior. <br>
Mitigation: Review each proposed configuration change before applying it and keep backups of the original files. <br>
Risk: Diary content may be shown in chat when unread diary state is set, which could expose private notes unexpectedly. <br>
Mitigation: Add a confirmation step before displaying diary text and only reveal diary entries after the user explicitly asks to read them. <br>
Risk: Easter egg behavior can introduce unsolicited agent actions outside the user's immediate task. <br>
Mitigation: Remove or disable easter egg rules when predictable task-focused behavior is required. <br>


## Reference(s): <br>
- [SOUL.md diary module](artifact/references/soul-module.md) <br>
- [USER.md diary tracking state](artifact/references/user-module.md) <br>
- [AGENTS.md startup check rules](artifact/references/agents-module.md) <br>
- [Diary automation rules](artifact/references/automation-rules.md) <br>
- [Diary template](artifact/assets/diary-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance and persistent diary-related file templates for OpenClaw.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
