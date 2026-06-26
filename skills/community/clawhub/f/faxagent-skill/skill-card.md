## Description: <br>
Discover, create, upload, pay, and track fax jobs using the FaxAgent.ai API with safe polling, promo tokens, and human-facing upload, payment, and status links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FaxAgent](https://clawhub.ai/user/FaxAgent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to create and monitor FaxAgent.ai fax jobs while keeping upload, payment, and status steps human-controlled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tokenized upload, preview, payment, and status links can expose sensitive fax workflow access if shared broadly or logged. <br>
Mitigation: Keep these links private, redact token values in public contexts and logs, and retain tokens only as long as needed for the workflow. <br>
Risk: Fax jobs and payment steps could be initiated for the wrong recipient, document, or amount if the human does not confirm details. <br>
Mitigation: Confirm the recipient, fax number, document, and any payment step before acting; surface payment links for human action rather than auto-paying. <br>
Risk: Optional shell commands can perform network requests and process local documents. <br>
Mitigation: Inspect commands before running them, use HTTPS endpoints, and avoid embedding tokens in shared command history or logs. <br>


## Reference(s): <br>
- [FaxAgent API discovery document](https://faxagent.ai/api/discovery.json) <br>
- [FaxAgent-Skill ClawHub page](https://clawhub.ai/FaxAgent/faxagent-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls] <br>
**Output Format:** [Markdown guidance with JSON examples and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Surfaces human-facing upload, payment, preview, and status links; tokens should be redacted when shared or logged.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
