## Description:

Recover from context compaction by scanning memory files and surfacing where an agent left off.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boscoeuk](https://clawhub.ai/user/boscoeuk)

### License/Terms of Use:


## Use Case:

Developers and agents use Context Anchor at session start, after context compaction, or during handoff to summarize current tasks, active context files, recent decisions, and open loops from local workspace memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell script accepts --days and DAYS_BACK without validating them as bounded positive integers before arithmetic.

Mitigation: Review or patch scripts/anchor.sh before installing; validate --days and DAYS_BACK as bounded positive integers before use.

Risk: Recovered memory and context files may contain stale, misleading, or adversarial content.

Mitigation: Treat the briefing as orientation data only and verify important claims against source files before acting.

Risk: File-derived text may affect terminal rendering when emitted through echo -e or similar formatted output.

Mitigation: Avoid echo -e for file-derived text or sanitize recovered content before displaying it.

## Reference(s):

- [Context Anchor ClawHub Skill Page](https://clawhub.ai/boscoeuk/skills/context-anchor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Terminal text briefing with Markdown-style sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local memory/current-task.md, recent memory/YYYY-MM-DD.md files, and context/active/*.md; no external services.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
