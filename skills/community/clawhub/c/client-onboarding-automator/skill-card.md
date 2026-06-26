## Description: <br>
Automates client onboarding from inquiry to project start, handling intake, contract creation, payment, welcome emails, and project setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[merjua14](https://clawhub.ai/user/merjua14) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Business operators, consultants, and service teams use this skill to coordinate client onboarding from a new inquiry through proposal, contract, payment, welcome messages, and project workspace setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client-facing emails, proposals, contracts, payment links, CRM updates, and delayed follow-ups may be sent or applied without adequate approval controls. <br>
Mitigation: Require manual approval before sending client-facing messages, contracts, proposals, payment links, CRM changes, or scheduled follow-ups. <br>
Risk: Payment and email integrations can expose sensitive credentials or allow broad actions if configured with over-permissive keys. <br>
Mitigation: Use scoped Stripe and email credentials, keep credentials out of prompts and shared files, and audit integration access regularly. <br>
Risk: Delayed onboarding messages can continue after a client changes scope, cancels, or opts out. <br>
Mitigation: Provide a visible way to cancel, pause, and audit delayed messages and reminders before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/merjua14/client-onboarding-automator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration examples and client-facing message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require email, Stripe, CRM, form, and workspace configuration before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
