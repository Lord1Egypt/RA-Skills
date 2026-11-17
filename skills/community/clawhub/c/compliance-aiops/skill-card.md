## Description:

Maps existing AIops audit trails to compliance controls and prepares coverage, gap, approval, exception, and integrity reports and evidence bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and compliance practitioners use it to review existing AIops audit records against HIPAA, PCI DSS, SOC 2, GDPR, ISO 27001, and DJCP L3 controls, identify evidence gaps, and prepare audit artifacts. Its reports describe recorded evidence and do not certify compliance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unintended or incomplete audit-source selection can produce incomplete evidence.

Mitigation: Review the selected sources and their time coverage before relying on a report or bundle.

Risk: Evidence files and signing secrets may expose sensitive information if mishandled.

Mitigation: Restrict access to evidence files and protect signing secrets.

Risk: Scheduled signing can create recurring signed evidence bundles.

Mitigation: Enable scheduled signing only deliberately.

Risk: Reports may be mistaken for a compliance certification.

Mitigation: Present results as evidence from audit trails, not as a compliance verdict.

Risk: An unexpected package release may be installed when setup requires internet access.

Mitigation: Verify the downloaded package version before use.

## Reference(s):

- [Compliance AIops on ClawHub](https://clawhub.ai/zw008/skills/compliance-aiops)
- [Project homepage](https://github.com/AIops-tools/Compliance-AIops)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, CSV, Shell commands]

**Output Format:** [Coverage, gap, approval, exception, and integrity reports; evidence bundles; suggested scheduling commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports reflect selected audit sources and time periods. Bundle integrity is tamper-evident, not tamper-proof.]

## Skill Version(s):

0.15.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
