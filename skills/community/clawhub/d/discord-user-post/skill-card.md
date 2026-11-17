## Description:

Post an approved message as the logged-in Discord user through the Discord desktop app. Use for release announcements or other direct user-authored Discord posts; not for OpenClaw channel sends, bots, webhooks, relays, agent sessions, or archive search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Discord users preparing release announcements or other direct, user-authored posts use this skill to publish an approved message through their existing logged-in desktop session to a verified server and channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A message could be posted from the wrong account or to the wrong server or channel, or its content could misrepresent the user.

Mitigation: Verify the visible logged-in account, server, and channel; show the exact message and obtain action-time confirmation before typing. Stop if the account or destination cannot be verified.

Risk: A duplicate or changed message could be sent after approval.

Mitigation: Enter the approved body unchanged, inspect the composed message and destination, send once, and reconfirm if the body or destination changes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/hillstreet-ph/skills/discord-user-post)
- [hillstreet-ph publisher profile](https://clawhub.ai/user/hillstreet-ph)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Approved Discord message text with a posting result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One approved message posted to the verified destination after action-time confirmation.]

## Skill Version(s):

1.0.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
