## Description:

TinkerClaw Agent Sensei is a reference field guide for AI agents covering ethics, messaging security, context and memory layout, configuration safety, scheduled jobs, multi-model routing, budget, bot collaboration, epistemic hygiene, and human-reviewed improvement proposals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[globalcaos](https://clawhub.ai/user/globalcaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill as reading material to compare their agent setup against practical operating guidance for safety, memory, configuration, scheduled jobs, collaboration, budget, and epistemic hygiene. It is intended for explicit read, teach, or comparison requests rather than automatic policy enforcement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational guidance about crons, memory, messaging, and configuration could be applied too broadly if treated as automatic policy.

Mitigation: Install and use the skill as reading material; apply any scheduled jobs, config changes, data sharing, or durable memory changes only after human review.

Risk: Guidance may be inappropriate for an agent setup with different permissions, platforms, or safety controls.

Mitigation: Compare the advice against the current system, developer, and user instructions before adopting it for a specific agent.

## Reference(s):

- [The Field Guide for New AI Agents](references/field-guide.md)
- [ClawHub skill page](https://clawhub.ai/globalcaos/skills/agent-sensei-ultimate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown prose with lists, tables, and examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reading material only; it does not execute, schedule, install, or persist changes by itself.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
