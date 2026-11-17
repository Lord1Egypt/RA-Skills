## Description:

douyin-spark helps an agent manage Douyin spark contacts and send configured private messages through a logged-in Douyin web session to maintain spark streaks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bazg3452-del](https://clawhub.ai/user/bazg3452-del)

### License/Terms of Use:

MIT-0

## Use Case:

Douyin users and OpenClaw agents use this skill to keep track of spark contacts, prepare renewal messages, and send those messages to selected contacts from an authenticated Douyin web session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad private-messaging authority through a logged-in Douyin session.

Mitigation: Require an explicit preview of recipients and exact message text before any message is sent.

Risk: Unattended scheduled runs could send messages to contacts without timely user review.

Mitigation: Avoid cron or HEARTBEAT-style unattended runs unless the workflow includes a fresh confirmation step.

Risk: The contact list and message text may contain personal or sensitive relationship data.

Mitigation: Keep the contact list limited to intended recipients and review the markdown contact file before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bazg3452-del/skills/douyin-spark)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Contact list template](artifact/contacts.example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline CLI commands and browser-action instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recipient names, message text, contact status, and per-contact send results based on a markdown contact list.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
