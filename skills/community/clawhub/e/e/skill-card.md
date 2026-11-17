## Description:

Short alias skill for editing files, code, or configurations. Use when you need to make changes to existing content using text editors or IDE shortcuts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlang-cn](https://clawhub.ai/user/openlang-cn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill as a shortcut for controlled edits to files, code, and configuration. It helps select an editor or editing workflow, apply small reversible changes, validate configuration syntax, and review diffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands or edits could modify or restore files the user did not intend to change.

Mitigation: Use the skill only on clearly identified files and review diffs before accepting changes.

Risk: Configuration edits could affect service startup or runtime behavior.

Mitigation: Run the relevant local syntax or format checks before restarting services or committing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlang-cn/skills/e)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline command snippets and editing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file-edit instructions, command examples, validation steps, and diff-review guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
