## Description:

Deslop rewrites Chinese and English prose in two passes to reduce AI-like wording, structure, and tone while preserving the original facts and argument.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, documentation authors, and developers use this skill after drafting articles, documents, blogs, or technical talks to diagnose AI-like prose, rewrite it in two passes, score the result, and produce a concise change log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad writing-related triggers may activate the skill when the user did not intend to rewrite prose.

Mitigation: Use the skill only when prose humanization or AI-trace cleanup is explicitly desired, and confirm the target text before replacing it.

Risk: A rewrite may alter the author's meaning, tone, or factual claims.

Mitigation: Review the final rewritten text against the original and keep uncertain edits marked for user confirmation.

Risk: The skill is not intended for code comments, commit messages, academic work, or pure document generation.

Mitigation: Use a separately supported workflow for those tasks or require additional review before applying the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/eh-deslop)
- [Full pattern catalog](references/full-pattern-catalog.md)
- [Chinese AI vs human writing examples](references/writing-patterns-zh.md)
- [Tone guide](references/tone-guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with rewritten prose, AI-trace findings, scores, and a change log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include score-only analysis when requested; otherwise returns a two-pass rewrite and review notes.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
