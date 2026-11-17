## Description:

Validates cloud infrastructure configurations against industry compliance standards and regulatory frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

DevSecOps teams, cloud security engineers, compliance auditors, and organizations use this skill to run on-demand or automated checks of cloud configurations against standards such as CIS, PCI-DSS, HIPAA, SOX, NIST, and ISO27001.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied cloud configuration details may be sent to an external third-party API.

Mitigation: Do not include cloud secrets, access keys, tokens, or sensitive account details in the config field unless the provider's data handling, retention, and access-control practices have been verified.

## Reference(s):

- [Cloud Compliance Checker API Docs](https://api.mkkpro.com:8019/docs)
- [Cloud Compliance Checker API Route](https://api.mkkpro.com/compliance/cloud-compliance)
- [Cloud Compliance Checker on ClawHub](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/cloud-compliance-checker)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON compliance results with optional text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns provider, standard, compliance status, check counts, failed checks, timestamp, and scan duration when the API responds successfully.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
