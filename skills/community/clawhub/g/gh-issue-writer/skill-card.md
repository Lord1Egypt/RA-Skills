## Description:

Draft well-structured GitHub issues from a description, error, or idea. Supports bug reports, feature requests, enhancements, and tasks. Optionally submits directly via the GitHub CLI or API. Use when someone says "write a GitHub issue", "open an issue for", "file a bug", "create a feature request", or describes a problem that needs to be tracked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to turn a bug, feature idea, enhancement, or task into a clear GitHub issue with a suitable title, structured body, and suggested labels. They can review the draft and optionally submit it to a repository after confirming the destination and issue details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An issue may disclose sensitive logs or credentials or be published to a repository with unintended visibility.

Mitigation: Review the destination repository and its visibility, inspect the complete issue, remove sensitive information, and confirm the details before publishing.

Risk: The documented Python API fallback references re.fullmatch without importing re.

Mitigation: Add the missing re import before using the Python fallback.

## Reference(s):

- [GitHub Issue Writer on ClawHub](https://clawhub.ai/djc00p/skills/gh-issue-writer)
- [GitHub issue templates documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown issue drafts with optional submission guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Issue type, repository, details, and optional labels or assignment depend on the user's context.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
