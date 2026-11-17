## Description:

Privacy-first Spring Boot code health diagnosis that detects security vulnerabilities, performance anti-patterns, code quality issues, and dependency risks across Java/Spring Boot projects and generates a structured severity-classified health report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallyface0](https://clawhub.ai/user/sallyface0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan Java and Spring Boot projects for security, reliability, performance, design, error-handling, convention, and dependency findings before review, release, or daily development work. It produces a Markdown health report with severity grouping, a health score, issue locations, risk explanations, and repair guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can persist unredacted secrets, credentials, connection strings, local paths, or source excerpts found in scanned code.

Mitigation: Review reports before committing, sharing, or archiving them; add report directories to .gitignore or store reports outside the source tree, and rotate any real credential reproduced in a report.

Risk: The scanner reads local project code and may suggest code changes.

Mitigation: Use it only on projects you are authorized to inspect, and require explicit review before applying any suggested or optional auto-fix.

## Reference(s):

- [Java/Spring Detection Rules](references/rules/java-spring.md)
- [Code Health Report Template](references/report-template.md)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [ClawHub Skill Page](https://clawhub.ai/sallyface0/skills/code-health-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown report with issue tables, severity sections, code snippets, health score, and repair guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written to the scanned project and may include source excerpts or detected secrets if present in the input code.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
