## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexeyvorobiev](https://clawhub.ai/user/alexeyvorobiev)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to add proactive behavior, persistent memory practices, onboarding flows, heartbeat routines, security hardening, and self-improvement guardrails to an AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory routines can accumulate broad personal or work context in local files.

Mitigation: Narrow the WAL and memory rules before use, and review what the agent writes to USER.md, MEMORY.md, SESSION-STATE.md, and working-buffer files.

Risk: Proactive routines may encourage autonomous local actions with too little user control.

Mitigation: Require confirmation before app, browser, file, email, calendar, repair, external communication, or publishing actions.

Risk: Self-modification guidance can change important agent behavior over time.

Mitigation: Require approval before modifying AGENTS.md, SOUL.md, skill files, or security-related rules.

## Reference(s):

- [Onboarding Flow Reference](references/onboarding-flow.md)
- [Security Patterns Reference](references/security-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/alexeyvorobiev/skills/alexey-proactive-agent)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown instructions with file templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes starter files for agent rules, identity, user context, memory, onboarding, heartbeat routines, tool notes, and a local security audit script.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact SKILL.md frontmatter declares 3.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
