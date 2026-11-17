## Description:

CHAT—Logger provides manual guidance for saving conversation turns to daily Markdown files in a workspace chat directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimyxu8812](https://clawhub.ai/user/jimyxu8812)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to keep a local, append-only Markdown history of user and assistant messages for backup, audit, journaling, or debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext conversation logs can capture secrets, credentials, regulated data, or confidential business information.

Mitigation: Use only with informed user consent, avoid sensitive conversations, and add redaction or encryption before using it in higher-risk workspaces.

Risk: Append-only daily files can retain conversation history longer than intended.

Mitigation: Define retention and deletion rules for the workspace chat directory before enabling routine logging.

Risk: Shared or synced workspaces can expose saved conversations to unintended readers.

Mitigation: Keep logs in private local workspace paths with restrictive permissions, or use protected storage when sharing or syncing is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimyxu8812/skills/autochatlogger)
- [ClawHub publisher profile](https://clawhub.ai/user/jimyxu8812)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript and shell code blocks; generated logs are Markdown files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill appends conversation entries to daily local files named YYYY-MM-DD.md.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
