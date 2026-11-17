## Description:

Automatic memory consolidation for OpenClaw agents that analyzes daily memory files, removes duplicates, prunes stale entries, normalizes dates, and builds a clean MEMORY.md index.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rimaslogic](https://clawhub.ai/user/rimaslogic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw agent operators use this skill to consolidate scattered daily memory files into a concise long-term MEMORY.md index, with duplicate removal, stale-entry pruning, date normalization, backups, and dry-run support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can repeatedly rewrite persistent agent memory.

Mitigation: Run dry-run mode first, inspect proposed memory changes, and keep independent backups before allowing writes.

Risk: The documented commands rely on an unaudited external package.

Mitigation: Use a pinned, auditable package version and review the installed package before execution.

Risk: Broad trigger phrases or heartbeat integration could cause recurring memory changes when not intended.

Mitigation: Avoid the broad "dream" trigger and enable heartbeat writes only when recurring memory maintenance is explicitly desired.

## Reference(s):

- [Autodream ClawHub skill page](https://clawhub.ai/rimaslogic/skills/autodream)
- [rimaslogic ClawHub publisher profile](https://clawhub.ai/user/rimaslogic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory maintenance guidance and examples for commands, configuration, heartbeat integration, consolidation reports, backups, and MEMORY.md output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
