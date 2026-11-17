## Description:

Code Reviewer helps review code changes, pull requests, or repositories across security, performance, code quality, error handling, testing, and documentation, with optional static analysis and HTML reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nameused](https://clawhub.ai/user/nameused)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review pull requests, diffs, files, or repositories and receive prioritized findings with remediation guidance. It can combine deterministic script output with checklist-driven reasoning for security, performance, quality, error handling, test, and documentation review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional HTML report can execute injected browser code when generated from untrusted finding data.

Mitigation: Open generated HTML reports cautiously for untrusted repositories or findings, or fix the escaping issue before using that report path.

## Reference(s):

- [Code Review Checklist](artifact/references/checklist.md)
- [Security Rules](artifact/references/security-rules.md)
- [Language-Specific Best Practices](artifact/references/best-practices.md)
- [Severity Guide](artifact/references/severity-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/nameused/skills/code-reviewer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with structured findings, optional JSON inputs, inline shell commands, and optional HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are grouped by severity and category; optional HTML reports should be treated cautiously for untrusted input.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
