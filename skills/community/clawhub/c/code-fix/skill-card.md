## Description:

Systematic code error diagnosis and fix skill for compilation errors, runtime exceptions, type errors, logic bugs, crash analysis, dependency conflicts, and unexpected behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to diagnose and repair code errors through a reproduce, isolate, understand, fix, and verify workflow. It is intended for debugging build failures, runtime exceptions, dependency issues, logic defects, and unexpected behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may suggest shell commands or project edits that affect repository state.

Mitigation: Review proposed commands and edits before execution, especially in sensitive repositories.

Risk: The skill includes examples for package-manager cleanup and unpinned package execution.

Mitigation: Confirm the project path, prefer lockfile-pinned local binaries, and explicitly approve dependency installation or destructive cleanup.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project edits, troubleshooting commands, and verification steps for the user's repository.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
