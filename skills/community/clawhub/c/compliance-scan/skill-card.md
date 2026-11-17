## Description:

Scans code repositories or data-processing flows for GDPR, CCPA, SOC 2, HIPAA, PCI-DSS, and related compliance risks, then produces structured reports and remediation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sh2601393743-png](https://clawhub.ai/user/sh2601393743-png)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, compliance officers, and technical leaders use this skill to perform repository-level privacy and security compliance self-checks and prepare audit-oriented remediation plans. It is a self-check aid and does not replace legal advice or a formal compliance audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compliance findings can be mistaken for legal advice or a formal audit result.

Mitigation: Use the report as a self-check aid and have qualified legal, security, or compliance reviewers confirm material conclusions before relying on them.

Risk: The skill reads user-scoped repository content, so an overly broad scan scope may expose sensitive code or data to the agent context.

Mitigation: Confirm the scan scope before use and provide only repositories, files, or snippets the user is authorized to analyze.

Risk: Static compliance pattern checks may produce incomplete or overstated findings if business context is missing.

Mitigation: Review each finding for concrete file locations, relevant business context, framework mapping, and actionable remediation before making changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sh2601393743-png/skills/compliance-scan)
- [Publisher profile](https://clawhub.ai/user/sh2601393743-png)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown report with tables, findings, code snippets, and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include severity ratings, compliance framework mappings, remediation recommendations, a prioritized roadmap, and an audit preparation checklist.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
