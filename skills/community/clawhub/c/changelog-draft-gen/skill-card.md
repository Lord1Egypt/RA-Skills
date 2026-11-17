## Description:

Generates a reviewable changelog draft from local Git commit history, with Markdown or JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to draft changelogs from local Git commits for review before publishing release notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README offers an unpinned download-and-run installation path.

Mitigation: Install the reviewed package artifact instead of running a remote script without verifying its contents.

Risk: The permission metadata does not accurately describe local Git execution and optional file writes.

Mitigation: Review the skill before installing, grant only the local access needed, and explicitly approve any changelog file output.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/changelog-draft-gen)

## Skill Output:

**Output Type(s):** [Markdown, JSON]

**Output Format:** [Markdown changelog draft or machine-readable JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prints to standard output by default; optionally writes a changelog file when requested. Review the draft before release.]

## Skill Version(s):

1.0.1 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
