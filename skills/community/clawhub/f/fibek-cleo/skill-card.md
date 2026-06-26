## Description: <br>
Interact with the Fibek B2B collections platform API to manage invoices, clients, payment agreements, campaigns, and financial metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fibekdev](https://clawhub.ai/user/fibekdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External collections and finance users use this skill to authenticate to a Fibek environment, review receivables, monitor client risk, manage payment agreements, send account statements or reminders, and inspect collections metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send customer communications and execute collections campaigns. <br>
Mitigation: Require human review before any reminder, account statement, WhatsApp or email message, or campaign execution. <br>
Risk: The skill depends on a trusted Fibek API environment and stores an authentication token for reuse. <br>
Mitigation: Set FIBEK_BASE_URL only to a trusted Fibek server and treat the stored token as a long-lived credential. <br>


## Reference(s): <br>
- [Fibek Cleo on ClawHub](https://clawhub.ai/fibekdev/fibek-cleo) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, markdown] <br>
**Output Format:** [Markdown responses with numbered Spanish-language summaries and structured API-driven workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses per-user authentication and the configured FIBEK_BASE_URL environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
