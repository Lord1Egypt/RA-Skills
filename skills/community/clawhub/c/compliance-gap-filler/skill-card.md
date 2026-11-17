## Description:

Identifies and fills compliance control gaps across security frameworks like ISO 27001, NIST, and SOC 2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Security teams, compliance officers, security architects, internal audit teams, MSSPs, and organizations preparing for certification audits use this skill to analyze missing compliance controls and receive remediation recommendations across frameworks such as ISO 27001, NIST CSF, SOC 2, PCI-DSS, and HIPAA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted compliance gaps may reveal sensitive security posture, audit, vulnerability, customer, or regulated information to a third-party API.

Mitigation: Confirm organizational approval and data-handling requirements before use, and submit only control identifiers or summaries that are approved for disclosure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/compliance-gap-filler)
- [API docs](https://api.mkkpro.com:8024/docs)
- [Kong route](https://api.mkkpro.com/compliance/gap-filler)
- [ToolWeb](https://toolweb.in)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Analysis, Guidance]

**Output Format:** [JSON responses with compliance gap analysis, severity ratings, implementation effort estimates, cross-framework references, and remediation recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a compliance framework name and a list of missing controls; calls an external third-party API.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
