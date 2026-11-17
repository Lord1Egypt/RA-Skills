## Description:

Intelligent disk space analysis and cleanup tool with safety grading, duplicate detection, and Chinese app cache recognition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and power users use this skill to inspect local disk usage, identify large or duplicate files, and review safety-graded cleanup recommendations before removing files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Safety guarantees may not be reliably enforced before scanning, hashing, or deleting files.

Mitigation: Review the skill before installing, use preview-only behavior until paths are inspected, and avoid elevated privileges.

Risk: Protected-path and no-content-reading claims should not be relied on as written.

Mitigation: Manually verify target paths and cleanup candidates before allowing any cleanup mode that changes files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/disk-sweeper)
- [Protected paths reference](references/protected-paths.json)
- [Cache patterns reference](references/cache-patterns.json)
- [File types reference](references/file-types.json)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown reports with optional JSON summaries and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on local filesystem paths, selected scan options, and cleanup mode; cleanup actions should be previewed before execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
