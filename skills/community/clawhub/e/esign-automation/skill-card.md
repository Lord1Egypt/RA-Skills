## Description: <br>
Automates eSignGlobal contract signing workflows through the eSignGlobal CLI, including draft envelope creation, sender view links, sending, reminders, cancellation, downloads, PDF signature verification, template rendering, contract comparison, attachment management, CC recipients, and signer changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[esign-cn-open-source](https://clawhub.ai/user/esign-cn-open-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate eSignGlobal e-signature workflows from an agent, including preparing and sending envelopes, checking status, managing recipients and attachments, rendering templates, comparing PDFs, downloading completed documents, and verifying signed PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can initiate sensitive e-signature actions such as sending, cancelling, reminding, or changing recipients. <br>
Mitigation: Verify the exact PDF, envelope ID, recipients, and requested action with the user before running the CLI command. <br>
Risk: The skill depends on an eSignGlobal API key for account-backed operations. <br>
Mitigation: Use a scoped API key where possible and do not print, store, or persist the API key in agent output or files. <br>
Risk: The skill invokes an external CLI through npx for contract workflows. <br>
Mitigation: For sensitive contract work, preinstall or pin a reviewed version of the eSignGlobal CLI before use. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/esign-cn-open-source/esign-automation) <br>
- [eSignGlobal website](https://www.esignglobal.com?source=agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and JSON command arguments; external CLI responses may be returned as JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 18 or later, the eSignGlobal CLI through npx, and ESIGNGLOBAL_APIKEY for API-backed actions.] <br>

## Skill Version(s): <br>
1.7.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
