## Description:

Access third-party services including Gmail, Slack, Google Calendar, GitHub, and custom Auth0 connections on behalf of authenticated users via Auth0 Token Vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deepu105](https://clawhub.ai/user/deepu105)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to search, read, send, or manage email, calendar, Slack, GitHub, and authenticated custom API workflows through the auth0-tv CLI. It is intended for cases where the user has connected accounts and wants the agent to act through those accounts with human-reviewed setup and destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform write-capable actions across connected email, Slack, Calendar, GitHub, and custom API accounts.

Mitigation: Use narrow OAuth scopes and manually review send, delete, post, update, and non-GET fetch requests before execution.

Risk: Custom Auth0 connections and raw fetch behavior may grant access beyond the built-in service workflows.

Mitigation: Restrict allowed domains, avoid broad custom connections, and connect only services needed for the user's specific task.

Risk: Setup can run through an unpinned npx installer path.

Mitigation: Prefer a pinned and reviewed setup package version before running installer commands.

Risk: Auth0 secrets, OAuth tokens, or account credentials could be exposed if pasted into chat.

Mitigation: Do not paste Auth0 secrets or tokens into chat; keep login and connection flows human-controlled.

## Reference(s):

- [Auth0 Token Vault Skill Page](https://clawhub.ai/deepu105/skills/auth0-token-vault)
- [Publisher Profile](https://clawhub.ai/user/deepu105)
- [auth0-tv Command Reference](references/commands.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are expected to use auth0-tv JSON output and require human interaction for login, connection setup, and OAuth flows.]

## Skill Version(s):

0.6.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
