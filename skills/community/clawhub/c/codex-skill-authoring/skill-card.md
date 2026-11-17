## Description:

Create, edit, and package new AgentSkills for English and Chinese skill-authoring requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddieguan801-oss](https://clawhub.ai/user/eddieguan801-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create, edit, structure, validate, and package modular AgentSkills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill authoring can create or modify persistent files in the OpenClaw workspace.

Mitigation: Review generated skill files before packaging or installing them.

Risk: The bundled listing utility can read installed skills' SKILL.md metadata and print names, descriptions, and paths when invoked.

Mitigation: Run the utility only in workspaces where listing installed skill metadata and paths is acceptable.

## Reference(s):

- [Skill Design Patterns](references/design-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/eddieguan801-oss/skills/codex-skill-authoring)
- [Publisher Profile](https://clawhub.ai/user/eddieguan801-oss)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent workspace files for skill source, references, scripts, and packaged skill archives.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
