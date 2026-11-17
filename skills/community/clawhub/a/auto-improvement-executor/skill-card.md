## Description:

Applies approved improvement candidates to target files, previews changes, and rolls back prior changes with automatic backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to apply accepted low-risk improvement candidates, preview file edits, and restore previous versions from receipts or backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The execution and rollback scripts can be steered by artifacts or command-line paths to modify or copy arbitrary writable local files.

Mitigation: Use only in a tightly controlled workspace, verify ranking and receipt artifacts plus target paths before execution, and run as a low-privilege user.

Risk: The --force option and rollback execution paths can bypass normal review expectations when inputs are not trusted.

Mitigation: Avoid --force and rollback execution unless paths and artifacts have been reviewed and the change is expected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/auto-improvement-executor)
- [Publisher profile](https://clawhub.ai/user/lanyasheng)
- [Skill definition](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON execution or rollback artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates backups, diffs, execution traces, and rollback pointers before modifying target files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
