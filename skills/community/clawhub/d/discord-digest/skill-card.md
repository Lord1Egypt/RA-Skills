## Description:

Generate formatted Markdown digests from selected Discord servers, channels, and threads using a Discord user token, with message summaries, source links, multi-server configuration, token validation, and configurable time periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikolaybohdanov](https://clawhub.ai/user/nikolaybohdanov)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to collect recent Discord activity from configured servers, channels, and threads and turn it into concise Markdown digests with links to source messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A full Discord user session token can expose the Discord account and private server content if mishandled.

Mitigation: Use the skill only with accounts and servers where this access is acceptable, avoid entering tokens directly in shell history, and prefer a limited-permission bot or OAuth flow when available.

Risk: The skill persists Discord token configuration locally.

Mitigation: Protect the local configuration directory, avoid plaintext token sharing, rotate the token if exposure is suspected, and remove the token when the skill is no longer needed.

Risk: Generated digests may include private community content and source links.

Mitigation: Restrict configured channels to non-sensitive spaces and get permission before forwarding digests to Telegram or other external services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nikolaybohdanov/skills/discord-digest)
- [Discord API v10](https://discord.com/api/v10)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown digest text with message links, plus JSON-like command output for setup and validation flows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Discord messages through a configured user token and selected server/channel settings; output is printed locally.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
