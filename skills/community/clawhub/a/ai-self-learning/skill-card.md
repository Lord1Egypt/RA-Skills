## Description:

AI自我改进与记忆系统 - 让AI从错误中学习，越用越聪明

This skill is ready for commercial/non-commercial use.

## Publisher:

[andylue](https://clawhub.ai/user/andylue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add a local memory workflow that records errors, user corrections, best practices, and knowledge gaps so future agent responses can reuse prior lessons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can save sensitive details from commands, errors, user corrections, and project context.

Mitigation: Use only with deliberate consent, avoid secrets or private context, and gate or redact memory writes before storage.

Risk: Stored memories can steer future agent behavior across projects.

Mitigation: Scope memory per project where possible and review retrieved memories before applying them to a new task.

Risk: The artifact describes syncing important memories into project instruction files.

Mitigation: Require explicit review before allowing the skill to modify CLAUDE.md, AGENTS.md, or similar project instruction files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andylue/skills/ai-self-learning)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline shell commands and optional text or JSON tool output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSONL memory files for errors, corrections, best practices, knowledge gaps, and an index.]

## Skill Version(s):

1.0.0 (source: server release metadata); artifact declares 2.0.0 in SKILL.md and skill.json

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
