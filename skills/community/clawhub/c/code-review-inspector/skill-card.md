## Description:

Automated code review checking for bugs, security issues, best practices, performance problems, and code style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michaelatamuk](https://clawhub.ai/user/michaelatamuk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review code changes before commits, pull requests, or security-sensitive releases. It produces prioritized suggestions for bugs, security issues, performance problems, maintainability, test coverage, and documentation gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent reads the code, diffs, or files the user asks it to review, which may include secrets or sensitive implementation details.

Mitigation: Install and use it only where code review access is appropriate; avoid supplying secrets, credentials, or unrelated sensitive files.

Risk: Review findings are suggestions and may be incorrect, incomplete, or overconfident for critical security issues.

Mitigation: Verify important findings with tests, scanner output, or human review before making release or security decisions.

Risk: The artifact includes security-example material containing vulnerable code snippets for illustration.

Mitigation: Treat examples as educational evidence, not executable behavior, and review any generated fixes before applying them.

## Reference(s):

- [Code Review Checklist](artifact/CODE_REVIEW_CHECKLIST.md)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/)
- [Refactoring Catalog](https://refactoring.com/catalog/)
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown review report with prioritized findings, explanations, and suggested fixes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity labels, file or line references when provided, code snippets, and follow-up validation recommendations.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
