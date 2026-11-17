## Description:

Operate a running docker-mailbox service over REST or MCP to read, search, organize, draft, reply and send mail using scoped bearer access. Use for mailbox tasks against a configured instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with a configured mailbox service: search and read email, organize messages, prepare drafts, and send or reply to mail through scoped REST or MCP access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setting up a Cloudflare Tunnel can expose the mailbox service beyond local access.

Mitigation: Use a tunnel only when remote access is intended; configure bearer authentication and narrow mailbox and operation scopes first, and protect tunnel credentials.

Risk: Mailbox configuration contains plaintext account passwords and bearer tokens.

Mitigation: Restrict file permissions, keep configuration and secrets out of source control and chat, and mount configuration read-only.

Risk: Deployment relies on trusting the Docker image source and release being used.

Mitigation: Verify the image source and release you intend to run before deployment.

## Reference(s):

- [Mailbox operations API reference](references/api.md)
- [Setup and deployment guide](references/setup.md)
- [Project homepage](https://github.com/psyb0t/docker-mailbox)
- [Upgrade notes](https://psyb0t.github.io/docker-mailbox/operations/#upgrade-notes)
- [Cloudflare Tunnel installation](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration]

**Output Format:** [Text and Markdown guidance, including API requests, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mailbox summaries, search results, draft content, and operation status]

## Skill Version(s):

1.2.10 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
