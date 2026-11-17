## Description:

CCPA Audit is a bilingual CCPA/CPRA compliance audit skill that previews privacy compliance checks and submits scored answers to the CQDev cloud engine at compliancehub.cn for report generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance teams, and privacy reviewers use this skill to run CCPA/CPRA checklist previews and generate cloud-scored compliance reports from their answers. It provides general compliance guidance and is not a substitute for legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scored audit runs send pass/fail CCPA answers to compliancehub.cn, including in anonymous trial mode.

Mitigation: Use preview mode when answer submission is not acceptable, and run scored audits only after confirming the cloud destination and data-sharing posture.

Risk: Anonymous trial mode stores a local trial identifier that can link trial usage over the seven-day quota window.

Mitigation: Delete ~/.config/compliancehub/ccpa-audit.anon_id if trial linkability is not desired.

Risk: HTML reports include cloud-returned content, and the security evidence notes that dynamic fields are not fully escaped.

Mitigation: Avoid opening HTML reports from untrusted or unexpected cloud responses until report rendering escapes dynamic fields.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwumit/skills/ccpa-audit)
- [ComplianceHub cloud service](https://compliancehub.cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands and generated text, JSON, or HTML audit reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scored runs submit audit answers to compliancehub.cn; preview mode fetches check items without submitting answers.]

## Skill Version(s):

2.1.0 (source: server release metadata, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
