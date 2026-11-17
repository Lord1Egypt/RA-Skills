## Description:

Code Reviewer helps developers review pull requests, git diffs, and code snippets for code quality, security vulnerabilities, performance issues, and best practices across Python, JavaScript/TypeScript, Java, Go, Rust, and Shell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review code changes before merging, check snippets for bugs or anti-patterns, audit common security issues, and improve code quality with actionable feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Code reviews may expose proprietary or secret-containing changes to the active agent session.

Mitigation: Use this skill only in workspaces and model sessions approved for the code, diffs, or PRs being reviewed.

Risk: Review findings can be incomplete or include false positives.

Mitigation: Treat findings as advisory and have a developer verify security, correctness, and performance concerns before merging changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ericlooi504/skills/eric-code-reviewer)
- [Publisher profile](https://clawhub.ai/user/ericlooi504)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown review findings with severity sections, line references when available, and optional inline fixes or patch guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect user-provided code, git diffs, branch comparisons, or PR content; local diff workflows require git.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
