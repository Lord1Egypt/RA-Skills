## Description:

Send and receive emails via API. Get a working email address instantly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dommholland](https://clawhub.ai/user/dommholland)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to send and receive email through the GetPost API without operating an email server. It covers API key creation, inbox retrieval, sending email, dedicated addresses, custom domains, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email content, inbound messages, and attachments may contain sensitive or untrusted data routed through GetPost.

Mitigation: Avoid sending secrets or regulated data unless the use is approved, and treat inbound bodies and attachments as untrusted.

Risk: A GetPost API key can authorize email actions if exposed.

Mitigation: Store the API key in a proper secret store and avoid hardcoding it in prompts, code, or shared logs.

Risk: Automated sending can deliver email to the wrong recipient or with incorrect content.

Mitigation: Confirm recipients, subject lines, and message bodies before sending email.

## Reference(s):

- [GetPost Email API documentation](https://getpost.dev/docs/api-reference#email)
- [ClawHub skill page](https://clawhub.ai/dommholland/skills/getpost-email)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with curl command examples and API endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GetPost API key; inbound email bodies and attachments should be treated as untrusted.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
