## Description: <br>
Generate customized compliance checklists for GDPR and PCI-DSS standards based on company type. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance teams, security officers, and organizations handling customer data or payment information use this skill to request a tailored GDPR and PCI-DSS checklist for their company type. The generated checklist supports risk assessment, audit preparation, and compliance program planning, but should be reviewed by qualified compliance, legal, or security staff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the provided company classification to an external ToolWeb/API provider. <br>
Mitigation: Submit only the minimum company classification needed and avoid including confidential business details in the request. <br>
Risk: Generated GDPR and PCI-DSS checklist items may be incomplete or unsuitable for a specific organization or jurisdiction. <br>
Mitigation: Have qualified compliance, legal, or security staff review the checklist before using it for audit readiness or compliance decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/gdpr-pci-checklist) <br>
- [Kong Route](https://api.mkkpro.com/compliance/gdpr-pci-checklist) <br>
- [API Docs](https://api.mkkpro.com:8015/docs) <br>
- [ToolWeb](https://toolweb.in) <br>
- [ToolWeb Portal](https://portal.toolweb.in) <br>
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/) <br>
- [RapidAPI Publisher Profile](https://rapidapi.com/user/mkrishna477) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON checklist items with compliance categories, requirements, standards, and status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a company_type request value and returns checklist content from an external ToolWeb/API provider.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
