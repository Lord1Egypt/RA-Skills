## Description:

Self-reflection, self-criticism, self-learning, and self-organizing memory for agents that evaluate their work, catch mistakes, and improve future responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[philippeliang](https://clawhub.ai/user/philippeliang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent a local, tiered memory process for explicit corrections, self-reflection, reusable preferences, and workflow lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local memory can influence future agent behavior across tasks.

Mitigation: Install only when cross-session steering is desired, use strict confirmation, and review ~/self-improving regularly.

Risk: Memory entries could capture sensitive or third-party information if boundaries are not followed.

Mitigation: Avoid storing credentials, health data, financial data, third-party information, or other sensitive content; use the documented forget and export controls.

Risk: Optional AGENTS.md, SOUL.md, and HEARTBEAT.md integrations can broaden the skill's steering effect.

Mitigation: Do not add those integrations unless persistent steering and maintenance behavior is explicitly wanted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/philippeliang/skills/claw-self-improving)
- [Skill homepage](https://clawic.com/skills/self-improving)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory files and agent operating guidance under ~/self-improving/ when installed and used.]

## Skill Version(s):

1.2.10 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
