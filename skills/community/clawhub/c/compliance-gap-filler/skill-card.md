## Description: <br>
Identifies and fills compliance control gaps across security frameworks like ISO 27001, NIST, and SOC 2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security teams, compliance officers, auditors, and MSSPs use this skill to analyze missing controls in frameworks such as ISO 27001, NIST CSF, SOC 2, PCI-DSS, and HIPAA and receive remediation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may send sensitive compliance posture details to an external API. <br>
Mitigation: Use only with an approved provider relationship and avoid submitting secrets, customer data, internal evidence, system names, or detailed audit weaknesses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/compliance-gap-filler) <br>
- [API documentation](https://api.mkkpro.com:8024/docs) <br>
- [Kong route](https://api.mkkpro.com/compliance/gap-filler) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON containing gap analysis, severity ratings, implementation effort estimates, cross-framework references, and summary guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a compliance framework string and an array of missing control identifiers or descriptions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
