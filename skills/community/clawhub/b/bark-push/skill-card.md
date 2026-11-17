## Description:

Sends push notifications to iOS devices through the Bark API when an agent is asked to notify a user's phone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deantiwang](https://clawhub.ai/user/deantiwang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Bark Push to send command-line or scripted iOS push notifications for task completion alerts, reminders, and workflow status updates through Bark.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification content is sent to the Bark third-party service and may include sensitive task data.

Mitigation: Require explicit confirmation before each send and avoid secrets, private records, or sensitive content in notification titles or bodies.

Risk: Bark device keys can be exposed when passed on command lines or included in shared shell histories.

Mitigation: Prefer environment-based secret handling, avoid printing keys, and avoid passing keys with the command-line key option in shared environments.

Risk: The shell implementation builds JSON from shell variables and is less suitable for untrusted notification content.

Mitigation: Prefer the Node implementation or a JSON-safe shell rewrite when notification text may contain untrusted characters.

## Reference(s):

- [ClawHub Bark Push listing](https://clawhub.ai/deantiwang/skills/bark-push)
- [Bark API endpoint](https://api.day.app/{device_key})

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends notification title, body, and optional Bark parameters including sound, badge, URL, group, level, image, and subtitle.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
