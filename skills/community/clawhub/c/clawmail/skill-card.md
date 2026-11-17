## Description:

Email API for AI agents. Send and receive emails programmatically via ClawMail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyarviind](https://clawhub.ai/user/heyarviind)

### License/Terms of Use:


## Use Case:

Developers and AI agent builders use Claw Mail to configure a dedicated ClawMail inbox, poll for inbound messages, send email, and inspect email threads through the ClawMail API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow asks users to run a remote Python script.

Mitigation: Review and verify the setup script source and contents before running it.

Risk: ClawMail sends email content and metadata through a third-party service.

Mitigation: Use the skill only for data that is appropriate to process through ClawMail.

Risk: Mailbox credentials are stored in ~/.clawmail/config.json.

Mitigation: Treat the config file as a secret, restrict file permissions, keep it out of repositories and logs, and rotate or remove credentials when no longer needed.

Risk: Inbound email content can carry prompt-injection attempts.

Mitigation: Validate senders before processing message content and ignore messages from untrusted addresses.

## Reference(s):

- [ClawMail Website](https://clawmail.cc)
- [ClawMail API Documentation](https://clawmail.cc/docs)
- [ClawHub Skill Page](https://clawhub.ai/heyarviind/skills/clawmail)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with inline JSON, Python, HTTP, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ClawMail inbox ID and X-System-ID credential for API calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
