## Description: <br>
Validates cloud infrastructure configurations against industry compliance standards and regulatory frameworks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
DevSecOps teams, cloud security engineers, and compliance auditors use this skill to check cloud configurations against compliance standards such as CIS, PCI-DSS, HIPAA, SOX, NIST, and ISO27001. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud configuration submitted for assessment is sent to an external API provider. <br>
Mitigation: Use sanitized configuration whenever possible, and do not submit cloud access keys, tokens, passwords, private account identifiers, or full sensitive infrastructure exports unless the provider's privacy, retention, and security practices have been reviewed. <br>


## Reference(s): <br>
- [OpenAPI Specification](artifact/openapi.json) <br>
- [API Docs](https://api.mkkpro.com:8019/docs) <br>
- [Compliance API Route](https://api.mkkpro.com/compliance/cloud-compliance) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, JSON] <br>
**Output Format:** [Markdown guidance with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Compliance requests include provider, standard, and optional configuration JSON; responses summarize pass/fail status, check counts, failed checks, timestamp, and scan duration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
