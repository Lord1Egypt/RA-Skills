## Description: <br>
Generates comprehensive cloud risk summaries by analyzing provider configurations, environments, services, and security exposures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security engineers, compliance teams, and DevSecOps professionals use this skill to submit cloud provider, environment, service, and exposure details and receive an executive risk summary with severity context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may send sensitive cloud exposure summaries to an external API. <br>
Mitigation: Redact secrets, credentials, raw customer data, internal identifiers, and unnecessary architecture details unless the organization has approved the provider and data-handling terms. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/krishnakumarmahadevan-cmd/cloud-risk-summary) <br>
- [Kong Route](https://api.mkkpro.com/compliance/cloud-risk-summary) <br>
- [API Docs](https://api.mkkpro.com:8027/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON response with summary text, risk level, provider, environment, exposure count, affected services, and analyzed exposures.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires provider, environment, services, and exposures in the request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
