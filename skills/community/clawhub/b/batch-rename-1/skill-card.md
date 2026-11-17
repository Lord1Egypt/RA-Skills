## Description:

Helps agents batch rename files using sequential numbering, find-and-replace, prefixes, suffixes, regex patterns, extension filters, and optional recursive processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1227323804](https://clawhub.ai/user/1227323804)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and file-management users use this skill to plan and run bulk filename changes across a selected folder. It is suited for renaming media, documents, or other local files with repeatable patterns while reviewing scope before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bulk rename operations can change many filenames at once and may be difficult to reverse.

Mitigation: Require a preview of each old and new path before execution, limit scope with extension filters, and confirm recursive operations explicitly.

Risk: Rename patterns may move files outside the intended folder if path separators, absolute paths, or parent-directory components are allowed.

Mitigation: Reject rename patterns containing path separators, absolute paths, or parent-directory components such as '..'.

Risk: The release security verdict is suspicious because containment for real bulk renames is not strong.

Mitigation: Use the skill only in trusted folders after review, and avoid recursive execution unless it is necessary and narrowly scoped.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1227323804/skills/batch-rename-1)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, JSON]

**Output Format:** [Markdown guidance with shell command examples and script JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script prints counts for renamed, skipped, and errored files plus old-to-new filename mappings.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
