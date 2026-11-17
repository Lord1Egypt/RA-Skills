## Description:

AI Code Reviewer helps analyze code quality, identify potential defects and security issues, generate PR descriptions, and suggest unit tests across multiple programming languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review code or diffs, identify quality, security, and performance issues, prepare PR descriptions, and draft unit test cases before merge or release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional API and GitHub credentials may expose repository access if configured with broad privileges.

Mitigation: Prefer read-only review first, use least-privilege or short-lived tokens, and keep GitHub Actions permissions minimal.

Risk: Automatic fixes or PR automation may introduce incorrect changes.

Mitigation: Review generated diffs, tests, and PR content before accepting or merging them.

Risk: Copied CI workflow examples may rely on mutable action references.

Mitigation: Pin copied GitHub Actions workflow steps to immutable commit SHAs before CI use.

## Reference(s):

- [AI Code Reviewer ClawHub Skill](https://clawhub.ai/daimingvip-a11y/skills/ai-code-reviewer)
- [AI Code Reviewer Documentation](https://clawhub.ai/docs/ai-code-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review reports, PR descriptions, test code snippets, shell command examples, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require code or diff input; optional PR automation depends on configured GitHub credentials.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
