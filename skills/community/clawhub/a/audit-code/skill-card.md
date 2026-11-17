## Description:

Security-focused code review for hardcoded secrets, dangerous calls, and common vulnerabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsnishi](https://clawhub.ai/user/itsnishi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan project code before commits, pull request reviews, periodic audits, or after AI-assisted code generation. It reports likely secrets, dangerous calls, dependency risks, sensitive files, file-permission issues, and exfiltration patterns with remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scans the selected project tree, including .env-like files, and its report may display matched secrets.

Mitigation: Run it only on projects you are authorized to audit, treat reports as sensitive, and redact or rotate exposed credentials before sharing results.

Risk: Package install names found in code may be checked against PyPI or npm over the network.

Mitigation: Run it in an environment where outbound registry lookups are acceptable, or manually review package findings when network access is restricted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itsnishi/skills/audit-code)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown security audit report with severity-ranked findings, file locations, matched patterns, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include sensitive matched text from scanned files; treat output as sensitive.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
