## Description: <br>
Assesses an organization's readiness for India's Digital Personal Data Protection Act 2023 by collecting questionnaire answers and returning ToolWeb API-backed scores, checklists, remediation roadmap, and executive summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Privacy, security, and compliance teams use this skill to assess DPDP readiness for organizations operating in India, identify gaps across seven privacy domains, and plan remediation. <br>

### Deployment Geography for Use: <br>
Global, for organizations with India privacy obligations. <br>

## Known Risks and Mitigations: <br>
Risk: Organization details and DPDP questionnaire answers are sent to ToolWeb's third-party API. <br>
Mitigation: Do not include secrets, customer records, or unnecessary sensitive details; protect TOOLWEB_API_KEY and review ToolWeb's billing, privacy, retention, and contractual terms before using real company data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/dpdp-compliance-assessment) <br>
- [ToolWeb platform](https://toolweb.in) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [ToolWeb OpenClaw skills](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style assessment summary with scores, domain breakdowns, priority gaps, and remediation actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls are submitted to ToolWeb for assessment and billing.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
