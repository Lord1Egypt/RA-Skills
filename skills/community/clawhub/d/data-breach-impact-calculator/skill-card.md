## Description: <br>
Calculate data breach costs, financial impact, regulatory fines, and remediation expenses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security, risk, compliance, insurance, and executive-reporting teams use this skill to estimate the financial impact of data breaches, including regulatory fines, notification costs, remediation, legal exposure, and reputation-related losses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends breach scenario details to the ToolWeb API. <br>
Mitigation: Do not submit raw PII, PHI, credentials, incident secrets, or unnecessary organization-specific details unless privacy, legal, and vendor review requirements are satisfied. <br>
Risk: Successful ToolWeb API calls may affect quota or billing. <br>
Mitigation: Monitor API usage and ensure the configured TOOLWEB_API_KEY is approved for the intended subscription and workload. <br>
Risk: The skill depends on ToolWeb API availability and a valid API key. <br>
Mitigation: If the API call fails, report the ToolWeb error to the user and avoid generating an unsupported breach-cost assessment from general knowledge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/data-breach-impact-calculator) <br>
- [ToolWeb API portal](https://portal.toolweb.in) <br>
- [Data Breach Calculator API endpoint](https://portal.toolweb.in/apis/security/data-breach-calculator) <br>
- [ToolWeb platform](https://toolweb.in) <br>
- [ToolWeb OpenClaw skills](https://toolweb.in/openclaw/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown breach-impact assessment with a curl API call] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TOOLWEB_API_KEY and curl; successful API calls may affect ToolWeb quota or billing.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; skill frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
