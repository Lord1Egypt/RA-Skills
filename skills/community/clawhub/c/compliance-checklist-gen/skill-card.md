## Description:

Generates industry-specific and region-specific compliance checklists to streamline regulatory adherence and audit preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, compliance officers, risk managers, and internal audit teams use this skill to request industry- and region-specific compliance checklists for audit preparation and governance planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends industry and jurisdiction values to a third-party provider API.

Mitigation: Use only high-level industry and region values unless the provider's privacy and retention terms have been reviewed.

Risk: Generated compliance checklists may be incomplete or unsuitable for a specific audit or regulatory obligation.

Mitigation: Have qualified compliance, legal, or audit personnel review checklist items before using them for regulatory decisions.

Risk: Submitting confidential audit evidence, secrets, internal control details, or regulatory findings could expose sensitive information.

Mitigation: Do not submit customer data, secrets, audit evidence, internal control details, or confidential findings through this skill.

## Reference(s):

- [Compliance Checklist Generator API Docs](https://api.mkkpro.com:8020/docs)
- [Compliance Checklist Generator API Route](https://api.mkkpro.com/compliance/checklist-generator)
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/compliance-checklist-gen)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON response containing checklist items, framework labels, status values, totals, and estimated completion hours.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires industry and region inputs; output depends on the provider API response.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
