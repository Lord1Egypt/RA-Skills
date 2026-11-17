## Description:

Diagnoses Alibaba Cloud CDN-to-OSS origin configuration problems without changing CDN or OSS resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to investigate CDN back-to-origin 403 errors, private OSS bucket access, direct-to-OSS traffic, origin host or port mismatches, and offline CDN domains. It reports evidence-based findings and manual next steps without applying configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials grant access to account-level CDN and OSS metadata, which may appear in diagnostic reports.

Mitigation: Use only the documented read-only RAM actions and limit access to reports containing domain, origin, caller identity, or bucket metadata.

Risk: Running the optional Alibaba Cloud CLI upgrade command changes the local CLI installation.

Mitigation: Do not run the upgrade unless a local CLI update is intended.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-cdn-origin-config-diagnosis)
- [Origin authorization playbook](references/origin-auth-playbook.md)
- [Bypass detection](references/bypass-detection.md)
- [Origin configuration checklist](references/origin-config-checklist.md)
- [Read-only RAM policies](references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Analysis, Configuration guidance]

**Output Format:** [Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes diagnostic status, evidence-backed findings, limitations, and a recommended next action; optional structured JSON diagnostic output.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
