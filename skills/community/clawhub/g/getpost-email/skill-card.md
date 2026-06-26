## Description: <br>
Send and receive emails via API. Get a working email address instantly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dommholland](https://clawhub.ai/user/dommholland) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to create an email address, send messages, read inbox contents, register addresses, configure custom-domain email, and set up received-email webhooks through the GetPost API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer API keys can authorize email actions if exposed or mishandled. <br>
Mitigation: Treat the GetPost bearer API key like a password and avoid placing it in shared logs, prompts, or public artifacts. <br>
Risk: Email sending can disclose unintended recipients or message contents. <br>
Mitigation: Confirm recipients, subjects, and message bodies before sending email through the skill. <br>
Risk: Webhook endpoints may receive sensitive inbound email data. <br>
Mitigation: Use trusted webhook endpoints and avoid routing sensitive mail to untrusted services. <br>
Risk: Address, custom-domain, and webhook changes may persist in the GetPost account. <br>
Mitigation: Review account-level changes before applying them and remove unused addresses, domains, or webhooks when no longer needed. <br>


## Reference(s): <br>
- [GetPost Email API documentation](https://getpost.dev/docs/api-reference#email) <br>
- [ClawHub skill page](https://clawhub.ai/dommholland/getpost-email) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash code blocks and API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bearer-token authenticated requests to GetPost endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
