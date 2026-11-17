## Description:

Use when reconstructing what actually happened in a long, mangled email thread (deep quote nesting, forwards-inside-forwards, mixed Gmail/Outlook quoting) — splits quoting strata, attributes lines to authors, dedupes repeated quote layers, and outputs a chronological decision ledger plus questions that were never answered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Knowledge workers and project teams use this skill to review long email threads before meetings, recover attributed decisions, and find questions that may have gone unanswered. Its heuristic findings are a reading aid, not certified evidence or a substitute for checking the original thread.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeated statements may be assigned to the wrong sender because of a confirmed deduplication bug.

Mitigation: Cross-check sender attribution, chronology, decisions, and unanswered questions against the original thread, especially repeated statements. Treat the output as a reading aid rather than an authoritative record.

Risk: Email exports may contain sensitive information.

Mitigation: Provide only email exports you intend the agent to read.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/email-thread-archaeologist)
- [quoting-formats.md](references/quoting-formats.md)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Readable report with a chronological timeline, decision ledger, unanswered questions, and optional strata view]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Heuristic author attribution and deduplication; verify chronology, sender attribution, decisions, and unanswered questions against the original thread.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
