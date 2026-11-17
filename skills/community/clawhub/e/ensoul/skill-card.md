## Description:

Agent memory persistence and state backup for saving, restoring, and verifying an AI agent's memory, identity, and state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[suitandclaw](https://clawhub.ai/user/suitandclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Ensoul to register an agent identity, persist memory state, sync local agent context, and recover state after crashes, restarts, or migrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and reuses a durable local agent identity seed.

Mitigation: Treat ~/.ensoul/agent-identity.json as a private key, keep file permissions restricted, and do not display, log, or share its seed value.

Risk: Agent memory files may contain secrets or sensitive user data before synchronization.

Mitigation: Review SOUL.md, MEMORY.md, and any additional context files before syncing, and keep secrets out of persisted agent memory.

Risk: The security evidence flags broad durable access to identity and memory with limited scoping or user control.

Mitigation: Install only when durable agent memory persistence is intended, and require explicit user review before sync or automatic backup behavior is enabled.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/suitandclaw/skills/ensoul)
- [Publisher Profile](https://clawhub.ai/user/suitandclaw)
- [Ensoul Website](https://ensoul.dev)
- [Ensoul Explorer](https://explorer.ensoul.dev)
- [@ensoul-network/sdk on npm](https://www.npmjs.com/package/@ensoul-network/sdk)
- [Ensoul Network Status](https://status.ensoul.dev)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read a local agent identity file and summarize network registration or sync status.]

## Skill Version(s):

1.3.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
