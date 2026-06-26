## Description: <br>
Generate a comprehensive DPDP Act implementation checklist with evidence tracker and roadmap. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Privacy, security, and compliance teams use this skill to create DPDP Act implementation plans, audit evidence trackers, executive summaries, and phased roadmaps tailored to an organization's data processing profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends organization and data processing details to the ToolWeb service. <br>
Mitigation: Avoid regulated, customer, employee, health, children-related, or confidential business details unless approved for third-party processing. <br>
Risk: The skill uses an API key for a third-party service. <br>
Mitigation: Use a scoped or revocable TOOLWEB_API_KEY and rotate or revoke it if access is no longer needed. <br>
Risk: Compliance outputs may be used for legal or audit planning decisions. <br>
Mitigation: Have qualified privacy, legal, or compliance reviewers validate the checklist and roadmap before relying on them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/dpdp-checklist-gen) <br>
- [ToolWeb Portal](https://portal.toolweb.in) <br>
- [DPDP Checklist API Endpoint](https://portal.toolweb.in/apis/compliance/dpdp-checklist) <br>
- [ToolWeb Platform](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown summary generated from ToolWeb API response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; outputs may include compliance checklist, implementation roadmap, evidence tracker, and executive summary.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
