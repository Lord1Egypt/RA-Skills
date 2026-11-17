## Description:

Send push notifications to iOS devices through the Bark app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yanbo92](https://clawhub.ai/user/yanbo92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a Bark key and send iOS push notifications from an agent through the Bark API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Bark device key is stored locally and can allow notification sending if exposed.

Mitigation: Treat ~/.bark/key as a secret, keep it owner-readable only, and rotate the Bark key if exposure is suspected.

Risk: Notification text is sent through the Bark API.

Mitigation: Avoid sending sensitive notification content unless the user is comfortable with that data flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yanbo92/skills/bark)
- [Bark project](https://github.com/Finb/Bark)
- [Bark API endpoint](https://api.day.app/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Bark API calls that send notification text to a configured device.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
