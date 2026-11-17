## Description:

Creates normative OpenClaw Reference files that describe narrow agent professions for agent creation and management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rodrigo09313](https://clawhub.ai/user/rodrigo09313)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent architects use this skill to interview users, validate specialization boundaries, and generate structured Reference Markdown for new agent professions. It is intended for Russian-language OpenClaw knowledge bases where references drive agent creation, routing, and role separation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated references are intended to be saved under OpenClaw KB/references/[specialization].md and could collide with an existing specialization path.

Mitigation: Review the generated reference path and compare it with existing references before saving.

Risk: The workflow is Russian-language and OpenClaw-specific, so it may produce unsuitable guidance outside that knowledge base structure.

Mitigation: Install and use it only for OpenClaw specialization-reference authoring workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rodrigo09313/skills/agent-reference-creator)
- [README](artifact/README.md)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown reference file with YAML frontmatter and ordered Russian-language sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated references target OpenClaw KB/references/[specialization].md and should be reviewed before saving.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
