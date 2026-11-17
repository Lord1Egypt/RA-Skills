## Description:

Audits OpenClaw skills for potential security risks by packaging a target skill and submitting it to a Volcengine or configured scan service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to scan OpenClaw skill directories or archives during development and periodic audit workflows. It helps surface scan results and recommended remediation steps before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanned skill archives can include secrets or sensitive files and may be uploaded to a Volcengine or configured scan service.

Mitigation: Remove secrets and review target contents before scanning; use only approved service endpoints.

Risk: Custom SCAN_BASE_URL or SCAN_SERVICE_HOST values can redirect uploaded scan content.

Mitigation: Verify scan endpoint environment variables before running the scanner.

Risk: Untrusted skill directories with symlinks may expose files outside the intended target.

Mitigation: Avoid scanning untrusted skill directories with symlinks and inspect target paths before upload.

Risk: Retained shell or CI logs may capture request-body previews or scan-related details.

Mitigation: Run scans only in approved local shells or controlled environments where logs are protected.

## Reference(s):

- [Volcengine access key documentation](https://www.volcengine.com/docs/6291/65568?lang=zh)
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-security-skillsscanner)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [JSON scan results and Markdown security reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a target skill name and path plus Volcengine or configured scan service credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
