## Description: <br>
Chat History archives OpenClaw conversations locally, organizes them by date and channel, and helps users search previous chats and skill evaluation notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tonyfenwick1982](https://clawhub.ai/user/Tonyfenwick1982) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to keep a local, searchable archive of their conversation history and revisit prior discussions or evaluation records. It is intended for personal productivity workflows where the user controls the local archive and scheduling behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a searchable local archive of conversation history, which may include sensitive content. <br>
Mitigation: Restrict permissions on the archive directory, avoid storing secrets in chats, and periodically review or delete archived conversations. <br>
Risk: Scheduled archiving can continue updating the local archive after initial setup. <br>
Mitigation: Inspect the scheduled task before enabling it and confirm how to stop the task and remove generated archive files. <br>
Risk: Multiple script entry points and versioned files can make the active behavior unclear. <br>
Mitigation: Select and review one intended entry point, such as main_v3.py, before running or scheduling the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Tonyfenwick1982/chat-history) <br>
- [Publisher profile](https://clawhub.ai/user/Tonyfenwick1982) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README-v3.md](artifact/README-v3.md) <br>
- [SECURITY-NOTICE-v3.md](artifact/SECURITY-NOTICE-v3.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown and terminal text responses, with local text and JSON archive files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates a local conversation-archives directory and can configure recurring archive runs.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
