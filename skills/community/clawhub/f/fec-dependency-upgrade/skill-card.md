## Description:

Guides developers through evidence-based diagnosis and validation of frontend build, runtime, UI, and API issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this release to diagnose frontend build failures, runtime errors, UI anomalies, and API problems, then document tested fixes. Despite the listing name, this version describes a debugging workflow rather than a dependency-upgrade workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic reports may expose secrets, request data, internal URLs, customer information, or private screenshots.

Mitigation: Review and redact sensitive logs, headers, request bodies, environment values, and screenshots before saving or sharing reports.

## Reference(s):

- [Diagnostic report template](references/report-template.md)
- [ClawHub skill listing](https://clawhub.ai/bovinphang/skills/fec-dependency-upgrade)
- [Project homepage (listed in package metadata)](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Code]

**Output Format:** [Markdown diagnostic report with evidence, hypotheses, fixes, and validation results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report saved as reports/debug-YYYY-MM-DD-HHmmss.md]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json, README.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
