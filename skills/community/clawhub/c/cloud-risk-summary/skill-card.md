## Description:

Generates comprehensive cloud risk summaries by analyzing provider configurations, environments, services, and security exposures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud security engineers, compliance teams, and DevSecOps professionals use this skill to turn cloud environment, service, and exposure details into executive-level risk summaries and remediation context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud environment names, service inventories, vulnerability descriptions, and business-impact details may be sensitive when sent to a third-party API.

Mitigation: Confirm organizational approval for this data sharing before use, and avoid submitting secrets, customer data, regulated records, or internal-only identifiers unless approved.

Risk: Generated severity and remediation summaries may influence operational prioritization.

Mitigation: Review generated summaries against the underlying cloud findings before using them for executive reporting or remediation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/cloud-risk-summary)
- [API docs](https://api.mkkpro.com:8027/docs)
- [Kong route](https://api.mkkpro.com/compliance/cloud-risk-summary)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON response containing a risk summary, risk level, affected services, exposure count, and analyzed exposures.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires provider, environment, services, and exposure issue-impact details as structured input.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
