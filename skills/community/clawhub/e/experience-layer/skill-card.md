## Description:

Skill Experience Layer - A failure-driven learning mechanism for OpenClaw agents that automatically accumulates lessons and best practices to avoid repeating mistakes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jilanfang](https://clawhub.ai/user/jilanfang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain JSON experience files that record failures, best practices, and tool-specific patterns so future OpenClaw runs can check relevant lessons before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent experience files can steer future tool use with stale, incorrect, or unreviewed lessons.

Mitigation: Review each experience entry before installation, keep the records compact, and remove outdated or duplicate guidance during maintenance.

Risk: Bundled production examples include hard-coded Feishu IDs, personal labels, and local filesystem paths.

Mitigation: Edit examples before using them as live memory; remove account-specific IDs, personal labels, and environment-specific paths.

Risk: Experience entries cover shell commands, messaging, cron jobs, and external APIs, where copied guidance can affect execution or communication behavior.

Mitigation: Treat experience records as untrusted notes and approve relevant entries before allowing them to influence tool calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jilanfang/skills/experience-layer)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and JSON experience records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable JSON templates and example experience records for edit, exec, Feishu/Lark, messaging, and cron workflows.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
