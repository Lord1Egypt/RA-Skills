## Description:

Dory-Proof Memory System gives AI agents a file-based memory pattern for preserving task intent, state, decisions, and recent work across context resets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinhartbiz](https://clawhub.ai/user/justinhartbiz)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up persistent workspace memory, task tracking, and continuity files for agents that lose context between sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist exact user prompts, which can store secrets, personal data, or business information in local memory files.

Mitigation: Use sanitized summaries or redaction rules for sensitive prompts, and define review and deletion rules for memory files before deployment.

Risk: Persisted memory and state files may later be treated as high-priority instructions, creating prompt-injection or stale-instruction risk.

Mitigation: Treat memory files as inert records, keep AGENTS.md authoritative for operating rules, and review state files before acting on stored instructions.

## Reference(s):

- [Implementation Guide](references/IMPLEMENTATION-GUIDE.md)
- [Anti-Patterns](references/ANTI-PATTERNS.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file-structure guidance and template content for agent memory workspaces.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
