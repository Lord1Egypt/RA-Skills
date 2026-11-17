## Description:

Search, read, export, hand off, clone, move, or rebind local Codex history stored under ~/.codex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[severinzhong](https://clawhub.ai/user/severinzhong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect local Codex sessions, export transcripts or handoff notes, clone or move threads between workspaces, and rebind local provider metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exports and handoff notes can expose sensitive local Codex history.

Mitigation: Treat exported files as sensitive, review their contents before sharing, and limit output paths and recipients to the intended scope.

Risk: History rewriting and bulk metadata changes can alter many local Codex records.

Mitigation: Run dry runs first, review scope counts and planned changes, rely on backups for write operations, and require explicit approval before applying dangerous edits.

Risk: The security verdict flags guardrail weaknesses around high-impact operations.

Mitigation: Avoid broad commands such as change-provider-all unless intended, and independently review dangerous edit plan files immediately before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/severinzhong/skills/codex-history-manager)
- [Command reference](artifact/references/commands.md)
- [Safety reference](artifact/references/safety.md)
- [Storage model](artifact/references/storage.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, jsonl, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus optional Markdown, JSON, or JSONL exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain sensitive local Codex history and should be reviewed before sharing.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
