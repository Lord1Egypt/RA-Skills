## Description:

Organize and maintain agent workspace directories by initializing structure, classifying files, auditing placement, cleaning content, and suggesting expansions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaql](https://clawhub.ai/user/zhaql)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent workspace maintainers use this skill to initialize workspace structure, classify files by purpose, audit placement, detect duplicate or stale content, and plan cleanup or directory expansion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace cleanup guidance can lead to incorrect bulk renames, moves, archives, pruning, or changes to installed skill and reference documents.

Mitigation: Require a clear proposed diff or file list and explicit approval before applying bulk file operations or changing installed skill materials.

Risk: Removing duplicate or stale content can discard information that still has unique value.

Mitigation: Prefer archiving over deletion unless the content is confirmed to be completely redundant.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaql/skills/agent-workspace-manager)
- [Document Classification Rules](references/classification-rules.md)
- [Workspace Structure Templates](references/structure-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with directory trees, tables, file recommendations, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include proposed workspace changes such as file moves, archives, renames, cleanup plans, and health reports.]

## Skill Version(s):

1.1.0 (source: release evidence and CHANGELOG, released 2026-03-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
