## Description:

Manage multiple OpenAI Codex accounts by saving and switching local tokens, comparing quota headroom, and optionally syncing saved Codex tokens into OpenClaw agent auth stores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[odrobnik](https://clawhub.ai/user/odrobnik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users with multiple Codex identities use this skill to save, switch, compare, and choose Codex account tokens by quota headroom, with optional explicit sync into OpenClaw agent auth profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill rewrites and duplicates live Codex credentials in local snapshots and, when requested, OpenClaw agent auth files.

Mitigation: Install and run it only on trusted machines, keep credential directories private, and review generated token snapshots before relying on them.

Risk: OpenClaw sync can propagate saved Codex tokens into agent auth stores.

Mitigation: Use sync --dry-run to preview planned writes and --agent <name> to limit which agents receive token updates.

Risk: Server security guidance flags incomplete account-name path containment and silent snapshot-write behavior.

Mitigation: Avoid untrusted or unusual account names and review saved account files after commands until path validation and silent persistence behavior are fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/odrobnik/skills/codex-account-switcher)
- [Setup instructions](SETUP.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Markdown usage guidance with shell commands plus plain text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads and writes local Codex and OpenClaw authentication files when the provided script commands are run.]

## Skill Version(s):

1.4.3 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
