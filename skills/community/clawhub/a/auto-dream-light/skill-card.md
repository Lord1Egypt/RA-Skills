## Description:

Lightweight, memory-safe Auto Dream workflow for OpenClaw that consolidates recent notes into existing memory files without replacing the user's current memory structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrgyan](https://clawhub.ai/user/mrgyan)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to run conservative memory consolidation over recent daily notes, preserve their existing MEMORY.md and memory/ structure, and keep an auditable dream log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and update local memory notes, which may affect future agent behavior if incorrect information is consolidated.

Mitigation: Use clear trigger commands and review memory-file diffs and any commit created after each run.

Risk: Low-value or duplicate notes could be written into long-term memory if a run is not reviewed.

Mitigation: Follow the documented skip rules and preserve the existing memory structure, recording skips in the dream log when no durable memory is found.

## Reference(s):

- [Adapted Auto Dream Plan](references/adapted-plan.md)
- [Manual Run Guide](references/manual-run.md)
- [Semi-Automatic Mode](references/semi-auto.md)
- [ClawHub Skill Page](https://clawhub.ai/mrgyan/skills/auto-dream-light)
- [Publisher Profile](https://clawhub.ai/user/mrgyan)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Concise Markdown summaries with file edits, shell commands, and configuration guidance when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local memory files and record dream-log entries; users should review diffs and commits after a run.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
