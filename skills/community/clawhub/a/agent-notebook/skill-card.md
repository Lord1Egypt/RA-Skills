## Description:

Agent Notebook installs a file-based memory system for OpenClaw agents using MEMORY.md, daily notes, a cron inbox, heartbeat routines, and optional scheduled extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marc69-69](https://clawhub.ai/user/marc69-69)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give OpenClaw workspaces persistent session context through local memory files, daily logs, inbox processing, and optional scheduled maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files can accumulate personal data, customer data, secrets, or API key locations that may be read in future sessions.

Mitigation: Keep MEMORY.md and daily notes limited to non-sensitive operational context, avoid storing secrets or private data, and load memory only in trusted direct sessions.

Risk: Optional cron and scheduled-task setup runs recurring scripts that modify local memory files.

Mitigation: Review the scheduled commands and workspace path before enabling automation, and avoid enabling cron or scheduled tasks until the security guidance concerns are manually constrained or fixed.

Risk: The cron inbox can move content from other sessions or agents into daily notes and longer-term memory.

Mitigation: Review inbox entries before promotion and require approval for entries that contain sensitive, external, or untrusted content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/marc69-69/skills/agent-notebook)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)
- [Tests README](artifact/tests/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and maintains workspace-local memory files when its scripts are run.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
