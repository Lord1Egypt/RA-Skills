## Description:

Audits an OpenClaw installation for exposed secrets, risky gateway settings, unsafe file permissions, network exposure, unencrypted keys, and risky skills, then produces JSON and HTML reports without showing secret values.

This skill is ready for commercial/non-commercial use.

## Publisher:

[il190502](https://clawhub.ai/user/il190502)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and administrators use this skill to review their installation's local security posture and identify remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit reports contain file paths and settings from the scanned installation.

Mitigation: Choose scan roots and the Git repository deliberately, keep reports private, or use --no-report to avoid saving them.

Risk: Heuristic audit results can miss issues and cannot guarantee that an installation is secure.

Mitigation: Treat passing checks as an initial review and supplement them with OpenClaw security diagnostics.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, HTML, Guidance]

**Output Format:** [Console summary and optional JSON and HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can be skipped with --no-report; secret values are omitted and home paths are redacted.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
