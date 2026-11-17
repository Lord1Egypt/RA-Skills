## Description:

Receive-only email addresses for AI agents via aiemailservice.com, with mailbox creation, message reading, long-polling for new mail, and automatic OTP extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tcgsync-git](https://clawhub.ai/user/tcgsync-git)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to create receive-only disposable mailboxes, read incoming messages, wait for verification emails, and extract verification codes during automated signup or account-recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incoming emails, OTPs, verification links, and password-reset links are handled by an external third-party mailbox service.

Mitigation: Use the skill only where trusting aiemailservice.com with those contents is acceptable, preferably for disposable or low-risk signups.

Risk: Using third-party mailboxes for important accounts, work accounts, financial services, or password recovery can expose sensitive access paths.

Mitigation: Avoid those account classes unless the third-party mailbox trust boundary has been explicitly reviewed and accepted.

Risk: Deleting a mailbox can remove messages that may still be needed.

Mitigation: Confirm retention needs before deleting any mailbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tcgsync-git/skills/automated-ai-email-setup)
- [AI Email Service](https://aiemailservice.com)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, API calls]

**Output Format:** [Markdown with API examples, JavaScript snippets, and cURL commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Receive-only mailbox workflow with API-key authentication, message retrieval, long-polling, and OTP extraction.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
