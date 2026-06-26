## Description: <br>
Ai Persona Os.Bak helps OpenClaw agents set up and maintain a persona-driven local workspace with markdown memory, onboarding presets, heartbeat routines, checkpointing, and optional automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Wu-XiaoLin](https://clawhub.ai/user/Wu-XiaoLin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and OpenClaw users use this skill to create a persistent agent persona workspace, capture working context in local markdown files, and run repeatable routines for setup, memory, heartbeat checks, escalation, and recovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent local memory about the user and their work, which can accumulate sensitive personal, operational, or business context. <br>
Mitigation: Keep secrets, credentials, regulated data, and unnecessary third-party personal details out of USER.md, MEMORY.md, daily logs, and checkpoints; periodically audit or delete stored memory. <br>
Risk: Optional cron jobs, channel scans, calendar or email access, Discord gateway changes, and proactive memory maintenance can expand what accounts or files the agent can access. <br>
Mitigation: Review every optional automation before enabling it, confirm the exact accounts and files in scope, and require explicit approval for cron jobs or gateway configuration changes. <br>
Risk: Server security evidence flags broad persistent memory and automation authority with under-scoped or inconsistent privacy and channel-access guidance. <br>
Mitigation: Install only when persistent local persona memory is desired, keep the workspace scoped, and review security guidance before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Wu-XiaoLin/ai-persona-os-bak) <br>
- [AI Persona OS homepage](https://jeffjhunter.com) <br>
- [Heartbeat Automation Guide](references/heartbeat-automation.md) <br>
- [Never-Forget Protocol](references/never-forget-protocol.md) <br>
- [Proactive Playbook](references/proactive-playbook.md) <br>
- [Security Patterns](references/security-patterns.md) <br>
- [SOUL.md Maker](references/soul-md-maker.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core setup uses local markdown files under ~/workspace; optional cron and gateway changes require explicit user opt-in.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.6.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
