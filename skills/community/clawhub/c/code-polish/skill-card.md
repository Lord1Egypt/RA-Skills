## Description:

Reviews local changes and GitHub pull requests before release, using project checks and multiple review passes to identify issues and recommend fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Polish before committing, pushing, or reviewing a pull request to find code quality issues and decide which fixes to make.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change source files before requesting the approval it promises.

Mitigation: Require Phase 1 to report validation failures without editing unless automatic fixes are separately authorized; preserve existing work and inspect project validation commands before execution.

## Reference(s):

- [ClawHub release](https://clawhub.ai/tenequm/skills/polish)
- [Project homepage (Clawdis metadata)](https://github.com/tenequm/skills/tree/main/skills/polish)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code]

**Output Format:** [Markdown review report with file and line references; source code edits when fixing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reviews local changes or a GitHub pull request; fix behavior depends on the selected mode.]

## Skill Version(s):

3.1.1 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
