## Description:

Scans Claude Code and OpenClaw skill directories, compares SKILL.md contents, and helps synchronize missing or conflicting skills with user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rushingai](https://clawhub.ai/user/rushingai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to compare local Claude Code and OpenClaw skill folders, review missing or divergent skills, and copy selected skill files between the two environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist unreviewed skill instructions into active Claude Code or OpenClaw skill folders.

Mitigation: Install only when skill-folder syncing is intended, review source skills before syncing, and avoid bulk actions for unknown skills.

Risk: Copied skill files can affect future agent sessions after synchronization.

Mitigation: Confirm conflicts deliberately and scan copied skills before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, files, configuration, guidance]

**Output Format:** [Markdown reports and prompts with file updates after confirmation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes SKILL.md and _meta.json files only for sync actions the user confirms.]

## Skill Version(s):

1.0.0 (source: frontmatter, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
