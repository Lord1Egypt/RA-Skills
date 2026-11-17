## Description:

Organizes files in a chosen directory by extension, previewing the plan by default and moving files into category folders only with --apply.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can preview how mixed files in a selected folder would be grouped by extension, then optionally move them into category subfolders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying a file-move plan may relocate important files unexpectedly.

Mitigation: Review a preview or --json report and back up important folders before using --apply.

Risk: Declared permissions understate the access required to organize files.

Mitigation: Review the skill and its local access requirements before installation or execution.

## Reference(s):

- [Directory Organizer on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/dir-organizer)
- [LGD theory referenced by the skill README](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [Plain-text or JSON file-move plan; category subfolders when applied]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires --dir; preview does not move files, while --apply moves files into category subfolders.]

## Skill Version(s):

1.0.5 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
