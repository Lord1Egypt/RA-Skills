## Description:

Send formatted notifications via email (himalaya) and iMessage (BlueBubbles). Use when you need to broadcast markdown-formatted messages to email recipients and phone numbers in a single step.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to draft a markdown message, format it with workspace tooling, and send it to email recipients or iMessage phone numbers from one command.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notifications may be sent to unintended email recipients or phone numbers.

Mitigation: Review the recipient lists and message content before running the notification command.

Risk: The skill relies on a local send-notification.sh script and configured email and iMessage accounts.

Mitigation: Confirm the local script implementation and account configuration are trusted before installation or use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/communication-assistant)
- [Publisher profile](https://clawhub.ai/user/terrycarter1985)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and argument tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions for sending user-provided markdown through configured email and iMessage accounts.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
