## Description:

Flutter Master helps agents build, review, refactor, debug, optimize, audit, test, and prepare Flutter and Dart mobile applications for release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anjasta-tarigan](https://clawhub.ai/user/anjasta-tarigan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill for Flutter and Dart implementation help, project audits, architecture review, state management decisions, performance troubleshooting, testing strategy, security review, and release readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local audit script can surface secrets, tokens, passwords, or other sensitive project details in a plain-text report.

Mitigation: Review reports locally and redact or rotate any exposed credentials before sharing output.

Risk: The script's grep-based checks may produce false positives or incomplete findings.

Mitigation: Treat scan output as candidates for human review and confirm each issue against the project before reporting it as a finding.

Risk: Flutter APIs and package recommendations can change over time.

Mitigation: Confirm current Flutter, Dart, and package behavior before recommending version-specific APIs or dependency changes.

## Reference(s):

- [Flutter Master skill page](https://clawhub.ai/anjasta-tarigan/skills/flutter-master)
- [Architecture](references/architecture.md)
- [Full Audit Checklist](references/audit-checklist.md)
- [Code Style & Effective Dart](references/code-style.md)
- [Performance](references/performance.md)
- [Release Checklist](references/release-checklist.md)
- [Security](references/security.md)
- [State Management](references/state-management.md)
- [Testing](references/testing.md)
- [UX Quality](references/ux-quality.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized audit findings and local scan command output interpretation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
