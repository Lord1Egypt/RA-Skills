## Description:

Assess data privacy compliance across 20 control areas with 63 controls covering governance, consent, security, breach response, vendor management, and cross-border transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external auditors, developers, and compliance teams use this skill to gather privacy control answers, call the ToolWeb privacy checklist API, and receive area scores with prioritized findings for privacy program assessment or audit preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privacy assessment answers and notes about organizational weaknesses are sent to portal.toolweb.in without a clear confirmation step.

Mitigation: Use the skill only when off-system disclosure is acceptable, avoid unnecessary sensitive free-form notes, and prefer a workflow with explicit confirmation for local-only or controlled disclosure needs.

Risk: Successful API calls are counted for billing and require a ToolWeb API key.

Mitigation: Use a least-privilege API key, configure it only where needed, and confirm billing expectations before running assessments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/data-privacy-checklist)
- [ToolWeb Portal](https://portal.toolweb.in)
- [Data Privacy Checklist API Endpoint](https://portal.toolweb.in/apis/compliance/data-privacy-checklist)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, configuration]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces area-by-area compliance scores, critical findings, priority actions, and API error guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
