## Description: <br>
AGENTS.md/IDENTITY/SOUL/USER periodic reload skill to keep context fresh (.md-only v1.1.2), prevent confusion in long sessions, edit HEARTBEAT.md, add a cron task, and auto-summarize MEMORY and ToDo state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kentaroid-bot](https://clawhub.ai/user/kentaroid-bot) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to keep long-running sessions oriented by periodically rereading identity, project, and user context files and distilling recent logs into persistent memory and prioritized tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring automation can repeatedly read personal or project context logs and rewrite persistent memory files. <br>
Mitigation: Install only when scheduled memory maintenance is intended, review the exact file permissions before enabling the cron task, and keep MEMORY.md and HEARTBEAT.md under version control or backup. <br>
Risk: Memory summaries may drift or preserve sensitive details from USER.md, identity files, or memory logs. <br>
Mitigation: Avoid storing secrets or sensitive personal details in files the skill reads, and periodically inspect or disable the scheduled job if summaries are no longer accurate or wanted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kentaroid-bot/agents-refresh-md) <br>
- [OpenClaw Skills Documentation](https://docs.openclaw.ai/skills) <br>
- [Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline cron JSON and file-edit examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide edits to MEMORY.md and HEARTBEAT.md and schedule a recurring refresh task.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
