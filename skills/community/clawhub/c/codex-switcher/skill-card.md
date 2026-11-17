## Description:

Local OpenClaw skill for managing multiple OpenAI Codex accounts through auth snapshots, including add, switch, current-account, quota, and token-refresh workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppaibb](https://clawhub.ai/user/ppaibb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage multiple local Codex account snapshots, switch the active Codex credentials, inspect current account and quota status, and refresh expiring tokens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles long-lived OAuth tokens, snapshot files, and auth-profile backups that function as account credentials.

Mitigation: Use it only in a trusted local environment, restrict access to ~/.openclaw to the local user, and do not expose snapshot, backup, access-token, or refresh-token contents in chat or logs.

Risk: Configurable OAuth endpoint overrides could leak credentials if the local environment is tampered with.

Mitigation: Leave CS_OAUTH_AUTHORIZE_URL and CS_OAUTH_TOKEN_URL unset except during deliberate testing, and verify the environment before starting an add or refresh flow.

## Reference(s):

- [Security Notes](references/security-notes.md)
- [Local Flow Sketch](scripts/README-local-flow.md)
- [Codex Switcher on ClawHub](https://clawhub.ai/ppaibb/skills/codex-switcher)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown guidance with shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may create or update local OpenClaw auth snapshot and auth profile files when the bundled shell command is run.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
