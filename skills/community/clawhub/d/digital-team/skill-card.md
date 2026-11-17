## Description:

Manages digital employee roles by creating role profiles, reading and updating persistent memory, and launching role-specific sub-agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cabbage1016](https://clawhub.ai/user/cabbage1016)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to create, list, launch, and maintain digital employee roles as sub-agents. It helps teams persist role profiles, long-term memory, current task state, and shared project knowledge across agent sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent role-memory files can carry secrets, stale assumptions, or instruction-like content into later sub-agent runs.

Mitigation: Keep memory files reviewable, avoid storing secrets, and audit memory before injecting it into future sub-agents.

Risk: User-provided role names are used when creating and checking workspace role paths.

Mitigation: Restrict role names to safe identifiers and review proposed paths before creating or updating role files.

Risk: Automatic memory updates can preserve incorrect conclusions or unwanted behavior after a task completes.

Mitigation: Confirm or review automatic memory changes before relying on them in later work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cabbage1016/skills/digital-team)
- [Publisher profile](https://clawhub.ai/user/cabbage1016)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, role-memory files, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update persistent role and knowledge files in the workspace.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
