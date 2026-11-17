## Description:

Guides evidence-based diagnosis and verification of frontend build, runtime, UI, and API problems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT-0

## Use Case:

Frontend developers use this skill to triage build failures, runtime errors, UI defects, and API or data issues, then test likely causes and document minimal fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Collected logs, requests, environment details, and saved reports may expose secrets, personal information, or private endpoints.

Mitigation: Use sanitized diagnostics and redact credentials, cookies, tokens, personal information, internal URLs, and sensitive payloads before saving or sharing reports.

## Reference(s):

- [Diagnostic report template](references/report-template.md)
- [ClawHub skill listing](https://clawhub.ai/bovinphang/skills/fec-debug-framework)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands]

**Output Format:** [Markdown diagnostic report with supporting commands and fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Timestamped report recording evidence, hypothesis checks, root cause, validation, and residual risk.]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
