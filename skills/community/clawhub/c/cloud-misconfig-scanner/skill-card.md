## Description: <br>
Automated security scanner for identifying and reporting misconfigurations across cloud infrastructure providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, DevOps engineers, cloud architects, and organizations with multi-cloud environments use this skill to request cloud configuration scans and receive findings about misconfigurations, compliance impact, and remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to submit cloud credentials to a third-party API. <br>
Mitigation: Use temporary, read-only credentials scoped to the minimum account, region, and resources required for the scan. <br>
Risk: Credential retention, logging, deletion, and provider security practices are not fully described in the available evidence. <br>
Mitigation: Independently verify the provider's security, privacy, logging, retention, and deletion practices before using sensitive or production environments. <br>
Risk: Long-lived or privileged credentials could increase blast radius if mishandled. <br>
Mitigation: Avoid root, admin, production, or long-lived credentials; revoke or rotate submitted credentials after use and monitor cloud audit logs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/cloud-misconfig-scanner) <br>
- [Cloud Misconfig Scanner API Route](https://api.mkkpro.com/security/cloud-misconfig-scanner) <br>
- [Cloud Misconfig Scanner API Docs](https://api.mkkpro.com:8018/docs) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, JSON, Guidance] <br>
**Output Format:** [JSON responses with scan identifiers, status, findings, severity, compliance impact, and remediation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires provider selection and provider-specific cloud credentials in the request body.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
