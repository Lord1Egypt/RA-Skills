## Description:

Performs structured code reviews with severity-ranked findings and deep multi-agent workflows for code, pull requests, merge requests, diffs, and patches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review source changes, pull requests, merge requests, and diffs for correctness, security, and reliability, then receive severity-ranked findings with supporting evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security assessment marks this release suspicious, citing an isolation warning, a possible mismatch between its review purpose and some evaluation commands, and one partially analyzed reference.

Mitigation: Clarify the flagged command mismatch. Avoid running reviewed project tests or setup steps on systems with sensitive files or credentials unless authorized and isolated in a disposable environment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/iliaal/skills/compound-eng-code-review)
- [Standard Review Process](references/standard-review-process.md)
- [Scope Resolution](references/scope-resolution.md)
- [Deep Review](references/deep-review.md)
- [Severity and Confidence](references/severity-and-confidence.md)
- [Reviewer Trust Boundary](references/reviewer-trust-boundary.md)
- [Security Test Coverage](references/security-test-coverage.md)
- [Composer Review](references/composer-review.md)
- [CVSS 3.1 Specification](https://www.first.org/cvss/v3.1/specification-document)
- [Composer Schema](https://getcomposer.org/doc/04-schema.md)
- [Composer Configuration](https://getcomposer.org/doc/06-config.md)
- [Composer Repository Priorities](https://getcomposer.org/doc/articles/repository-priorities.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown code review with severity-ranked findings and supporting evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports scope, coverage, residual risks, and observed checks as applicable.]

## Skill Version(s):

5.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
