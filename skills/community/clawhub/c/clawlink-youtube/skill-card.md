## Description:

Manage YouTube channels, videos, comments, playlists, and creator workflows via the YouTube Data API v3.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, channel operators, and agents assisting them use this skill to inspect YouTube channel and video data, manage metadata, playlists, comments, subscriptions, and analytics, and follow OAuth-backed ClawLink workflows for YouTube operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth access uses the connected Google or YouTube account and may expose channel data or enable account-scoped actions.

Mitigation: Confirm the requested Google/YouTube OAuth permissions before connecting and revoke the YouTube connection or remove the plugin when it is no longer needed.

Risk: Write operations can create, update, moderate, or delete YouTube resources if approved by the user.

Mitigation: Preview write actions, confirm the target resource and intended effect, and reserve destructive actions for explicit user approval.

Risk: The skill depends on the external ClawLink plugin and hosted connection service for authentication and tool access.

Mitigation: Verify that clawhub:clawlink-plugin is the intended plugin and use ClawLink connection-management tools to confirm YouTube is connected before taking action.

## Reference(s):

- [YouTube Data API v3](https://developers.google.com/youtube/v3)
- [YouTube API Reference](https://developers.google.com/youtube/v3/docs)
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/skills/clawlink-youtube)
- [Publisher Profile](https://clawhub.ai/user/hith3sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the live ClawLink YouTube tool catalog as the source of truth for available operations.]

## Skill Version(s):

0.2.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
