## Description:

Apple Mail search on macOS with fast metadata and full body lookup for finding messages in Mail.app by subject, sender, recipient, date, opening messages, and reading full body text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gumadeiras](https://clawhub.ai/user/gumadeiras)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and macOS users use this skill to search local Apple Mail messages by subject, sender, recipient, date, and unread state, then read or open matching messages. It supports read-only mail discovery workflows and does not compose or send email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a globally installed, unpinned third-party npm CLI that can read local Apple Mail metadata and full message bodies.

Mitigation: Review the fruitmail package and publisher before installing, pin an audited version or use an isolated install, avoid sudo, and enable it only on Macs where local email access is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gumadeiras/skills/apple-mail-search-safe)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with inline shell commands; JSON may be returned when the underlying fruitmail command uses --json.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS Mail.app data and the fruitmail CLI; the documented behavior is read-only search and message body lookup.]

## Skill Version(s):

5.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
