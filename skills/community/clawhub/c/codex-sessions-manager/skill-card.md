## Description:

Codex Sessions helps agents inspect, search, export, verify, clean up, delete, restore, and purge local Codex sessions stored under a Codex root such as ~/.codex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1939869736luosi](https://clawhub.ai/user/1939869736luosi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to manage local Codex conversation history through MCP tools or CLI commands, especially when listing, exporting, deleting, trashing, restoring, purging, verifying, or diagnosing sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or permanently remove local Codex session history when destructive actions are confirmed.

Mitigation: Use preview mode first, prefer recoverable trash deletion over permanent delete, and require explicit confirmation before write operations.

Risk: A wrong Codex root could cause operations to inspect or modify unintended session storage.

Mitigation: Run doctor or inspect_root before delete, restore, purge, or cleanup, and verify the selected Codex root.

Risk: Side conversations are separate child sessions and may not be covered by operations on the parent session.

Mitigation: Identify child session IDs and preview all intended IDs together before confirming export, delete, trash, restore, purge, or verification.

Risk: Dependency changes in a globally installed CLI can affect local execution behavior.

Mitigation: Review npm dependency updates as with any globally installed CLI before installation or upgrade.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1939869736luosi/skills/codex-sessions-manager)
- [Safety Guide](docs/SAFETY.md)
- [README](README.md)
- [Skill Instructions](SKILL.md)
- [npm Package](https://www.npmjs.com/package/codex-sessions-manager)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute local session-management actions through MCP or CLI; destructive write paths require preview or explicit confirmation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
