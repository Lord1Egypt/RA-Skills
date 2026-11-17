## Description:

Use to talk to the Discord-backed OpenClaw agent/session; not for archive search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to ask questions of the Discord-backed OpenClaw session or route a post through it after selecting the target and delivery mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign with no reported findings, but analysis was partial because three referenced local paths were not found in the bundle.

Mitigation: Review the missing paths and install only if you trust the publisher and need the skill.

Risk: The skill can route content to a Discord-backed agent or publish/send messages through that route.

Mitigation: Resolve and check the target and delivery mode, then review the message content before sending; use force-send only when explicitly requested.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hillstreet-ph/skills/discord-clawd-agent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance and shell commands, with routed request or post text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route messages through a Discord-backed agent/session.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
