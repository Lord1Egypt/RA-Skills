## Description:

Git-based version control for OpenClaw system configuration changes, including creating checkpoints before sensitive operations and rolling back when recovery is needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welkeyever](https://clawhub.ai/user/welkeyever)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to create Git checkpoints before changing configuration, installing or removing skills, or editing core OpenClaw files. They can also use it to inspect history and roll back configuration state after a failed or unwanted change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can commit broad OpenClaw configuration state, which may capture sensitive files or unwanted runtime data if exclusions are incomplete.

Mitigation: Verify .gitignore before saving, scan changed files for secrets, prefer targeted git add commands, and review staged diffs before committing.

Risk: Rollback workflows can invoke destructive hard resets that permanently discard uncommitted changes.

Mitigation: Prefer soft or mixed resets, show exactly what would be lost, and require explicit human confirmation before any hard reset.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/welkeyever/skills/config-checkpoint)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
