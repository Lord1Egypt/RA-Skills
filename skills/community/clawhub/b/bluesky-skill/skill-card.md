## Description:

Manage a Bluesky account via the AT Protocol, including posts, replies, likes, reposts, follows, blocks, mutes, search, timelines, threads, notifications, direct messages, and profile updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johannesseikowsky](https://clawhub.ai/user/johannesseikowsky)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate a Bluesky account from a command-line tool, including publishing posts, engaging with timelines, handling notifications and direct messages, managing social relationships, and updating profile details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authority over a Bluesky account, including posting, deleting posts, changing social relationships, updating profile details, and accessing direct messages when enabled.

Mitigation: Install only for agents that should manage the account, use a dedicated app password, and avoid enabling direct-message access unless it is required.

Risk: Authentication uses a reusable session token cached at ~/.bsky_session.json.

Mitigation: Run the tool in an isolated environment and protect or delete the session cache after use or after revoking access.

Risk: The security evidence recommends caution with dependency handling before granting account credentials.

Mitigation: Use pinned dependencies and validate the runtime environment before supplying Bluesky credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johannesseikowsky/skills/bluesky-skill)
- [Bluesky app passwords](https://bsky.app/settings/app-passwords)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance, Configuration]

**Output Format:** [JSON objects from CLI commands with Markdown setup and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, BLUESKY_HANDLE, and BLUESKY_APP_PASSWORD; commands may read or modify Bluesky account state.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
