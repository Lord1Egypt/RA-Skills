## Description:

Guides a seven-phase review of a codebase for German GDPR/DSGVO privacy and compliance gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bergschloss](https://clawhub.ai/user/bergschloss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and privacy reviewers use this skill to identify potential gaps in personal-data handling, consent, data subject rights, retention, processors, and security controls in German-oriented applications.

### Deployment Geography for Use:

Germany

## Known Risks and Mitigations:

Risk: A broad trigger can start a full-repository review that encounters secrets, customer data, or confidential code.

Mitigation: Confirm the requested audit scope before running; avoid sensitive repositories unless such a review is authorized.

Risk: Detailed audit reports are written to the user's Desktop, and high-severity findings may be shared with review subagents.

Mitigation: Confirm report storage and any subagent review are acceptable before auditing sensitive material.

Risk: Code inspection alone cannot establish legal compliance or verify procedural requirements.

Mitigation: Have a qualified privacy or legal reviewer validate findings and current legal requirements before relying on the report.

## Reference(s):

- [ClawHub release: dsgvo-audit](https://clawhub.ai/bergschloss/skills/dsgvo-audit)
- [Server-resolved GitHub source](https://github.com/Bergschloss/dsgvo-audit)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown phase reports and consolidated audit summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source locations and include severity and suggested remediation. Reports are written outside the audited repository.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
