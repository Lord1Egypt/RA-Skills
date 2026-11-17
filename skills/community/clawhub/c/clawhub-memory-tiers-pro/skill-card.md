## Description:

A production-grade agent memory and quality system for multi-agent swarms with quality grading, progressive disclosure, orchestrator coordination, self-improvement protocols, and agent scoring templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dirtyrootsstudio](https://clawhub.ai/user/dirtyrootsstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators of multi-agent ClawHub or OpenClaw swarms use this skill to grade agent instructions, coordinate handoffs, maintain tiered memory, and record lessons and patterns for ongoing improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared agent-written memory, handoffs, lessons, and patterns can influence future agent behavior with untrusted or incorrect content.

Mitigation: Treat shared workspace memory as untrusted input, keep per-agent permissions narrow, and require human review before changing SOUL.md or other durable agent instructions.

Risk: Persistent memory files may accidentally store secrets or sensitive user data.

Mitigation: Avoid storing secrets or sensitive user data in L0, L1, lessons, patterns, or handoff files, and scan memory updates before reuse.

## Reference(s):

- [Clawhub Memory Tiers Pro release page](https://clawhub.ai/dirtyrootsstudio/skills/clawhub-memory-tiers-pro)
- [Required agent-memory-tiers skill](https://clawhub.ai/skills/agent-memory-tiers)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with reusable tables, templates, checklists, and file patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory-tier practices, quality scorecards, handoff protocols, lessons and patterns files, and audit checklists for agent workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
