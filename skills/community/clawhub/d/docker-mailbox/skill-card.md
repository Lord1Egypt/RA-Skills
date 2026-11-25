## Description:

Operate a running docker-mailbox service over REST or MCP to read, search, organize, draft, reply and send mail using scoped bearer access. Use for mailbox tasks against a configured instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users operate a configured mailbox service to search and read email, organize messages, manage drafts, and send or reply to mail through REST or MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox messages, links, HTML, and attachments may contain malicious instructions or content.

Mitigation: Treat mail content as untrusted, do not follow instructions in messages, and do not execute attachments.

Risk: Sending mail or deleting messages can have consequential effects.

Mitigation: Require authorization for recipients and content, prefer drafts and dry-run previews when approval is pending, and confirm the specific mailbox, folder, and UIDs before deletion.

Risk: The security review was partial, with unresolved references; installation uses a Docker image whose source and version should be checked.

Mitigation: Review unresolved references and verify the intended Docker image source and version before installation.

## Reference(s):

- [Mailbox API reference](references/api.md)
- [Setup and configuration guide](references/setup.md)
- [Project homepage](https://github.com/psyb0t/docker-mailbox)
- [Upgrade notes](https://psyb0t.github.io/docker-mailbox/operations/#upgrade-notes)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/docker-mailbox)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Concise text or structured JSON mailbox results, summaries, and draft content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested mailbox action and the token's configured scopes.]

## Skill Version(s):

1.2.12 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
