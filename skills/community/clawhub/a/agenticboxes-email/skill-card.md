## Description: <br>
Send and receive email as an agent via the agenticboxes HTTP API — one API key, no IMAP/SMTP setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenticbrian](https://clawhub.ai/user/agenticbrian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to give an agent a hosted email address for sending messages, receiving replies or signup confirmations, and managing related AgenticBoxes account workflows over HTTP. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets agents access and act on external mailbox content, including sensitive messages, replies, signup confirmations, and 2FA or account-recovery mail. <br>
Mitigation: Use least-privilege API keys, keep mailbox access scoped to the task, and avoid routing secrets, 2FA codes, or account-recovery mail through the agent unless a human explicitly approves it. <br>
Risk: The skill includes account creation, domain registration, credit top-ups, payment-linked actions, box deletion, outbound outreach, and DNS changes. <br>
Mitigation: Require human confirmation before spend, registration, account-destructive actions, outbound campaigns, or DNS modifications; set spend and credit limits where possible. <br>
Risk: API keys and webhook signing secrets can expose mailbox control or event payload integrity if mishandled. <br>
Mitigation: Treat AGENTICBOXES_API_KEY and webhook secrets as sensitive credentials, store them outside prompts and logs, rotate webhook secrets when exposed, require HTTPS callbacks, and verify webhook signatures. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agenticbrian/agenticboxes-email) <br>
- [Publisher Profile](https://clawhub.ai/user/agenticbrian) <br>
- [AgenticBoxes OpenAPI Spec](https://www.agenticboxes.email/openapi.yaml) <br>
- [AgenticBoxes Service Manifest](https://api.agenticboxes.email/.well-known/agentic.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples, endpoint descriptions, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include API request examples, event polling guidance, webhook setup steps, DNS record instructions, and operational cautions for mailbox and account actions.] <br>

## Skill Version(s): <br>
1.4.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
