## Description:

Bark notification assistant for sending text, links, images, and mixed content to one or more Bark users with configuration, history, update, and delete support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liberalchang](https://clawhub.ai/user/liberalchang)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to send, update, delete, and review Bark push notifications across configured users or groups from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Device keys, notification bodies, clipboard values, and local history may expose sensitive information.

Mitigation: Treat device keys as credentials, avoid sensitive notification or clipboard content, and restrict permissions on the .bark-push state directory.

Risk: A custom or untrusted Bark server can receive notification content and device keys.

Mitigation: Use a trusted HTTPS Bark endpoint for default_push_url and avoid HTTP or unknown custom endpoints.

Risk: Broadcast, update, and delete commands can affect unintended recipients or messages.

Mitigation: Manually confirm recipients and push IDs before using --user all, --update, or --delete; disable update/history when not needed.

## Reference(s):

- [Bark Official Website](https://bark.day.app)
- [Bark API Documentation](https://bark.day.app/#/tutorial)
- [ClawHub Skill Page](https://clawhub.ai/liberalchang/skills/barkpush)
- [Publisher Profile](https://clawhub.ai/user/liberalchang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets; runtime output is plain text status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send Bark API requests and may write local configuration and notification history under the configured state directory.]

## Skill Version(s):

1.2.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
