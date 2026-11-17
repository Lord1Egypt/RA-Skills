## Description:

Empathic Trinity Core installs, migrates, and configures a low-context OpenClaw memory system that uses session-first working memory, summary-style daily notes, compact long-term memory, and on-demand retrieval while preserving user-state and collaboration cues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chiyuchen-web](https://clawhub.ai/user/chiyuchen-web)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw workspace maintainers use this skill to migrate an existing workspace to a lower-context memory workflow, configure long-term and daily memory files, and guide agents toward concise, need-based memory retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to rewrite persistent memory and agent-instruction files before the user has reviewed the intended changes.

Mitigation: Review the planned edits to AGENTS.md, MEMORY.md, SOUL.md, USER.md, and daily memory files before applying them.

Risk: Broad workspace permissions could allow memory migration steps to affect more files than intended.

Mitigation: Use a backup or clean commit before installation and grant only the file access needed for the confirmed migration.

Risk: Memory migration can preserve outdated, sensitive, or misleading personal context if summaries are accepted without review.

Mitigation: Inspect the resulting MEMORY.md and daily summaries, remove sensitive or stale content, and keep only high-value long-term information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chiyuchen-web/skills/empathic-trinity-core)
- [Memory V8 README](artifact/README.md)
- [Memory V8 Architecture](artifact/ARCHITECTURE.md)
- [Daily memory guidance](artifact/daily/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with file-editing guidance and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace memory structure guidance and may direct changes to persistent agent and memory files.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
