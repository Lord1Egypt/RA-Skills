## Description:

Manages AI agent team members with roles, skills, leader assignment, expertise lookup, task delegation, and multi-agent workflow coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[realqiyan](https://clawhub.ai/user/realqiyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain a shared roster of AI agents, designate a leader, and route tasks based on roles, expertise, and availability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent team data and workflow rules can influence leader-agent behavior across sessions.

Mitigation: Install only when this behavior is intended, keep ~/.agent-team/team.json writable only by trusted users, and review team fields before use.

Risk: Team fields may contain instructions or sensitive content that affect agent behavior.

Mitigation: Avoid storing instructions or secrets in team fields, and disable load_workflow when workflow injection is not needed.

Risk: Resetting team data can remove shared team configuration.

Mitigation: Back up team data before using reset, or use a custom data-file path for isolated testing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/realqiyan/skills/agent-team-skill)
- [Plugin Installation Guide](https://github.com/realqiyan/agent-team-skill/blob/master/integrations/openclaw/agent-team/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text CLI output with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes team data in JSON at ~/.agent-team/team.json by default; supports a custom data-file path.]

## Skill Version(s):

2.1.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
