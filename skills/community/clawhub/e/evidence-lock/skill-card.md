## Description:

Write or rewrite a document in evidence-locked mode: no unsourced sentences; every substantive claim carries a footnote citing the exact passage in the user's provided sources, and anything unsupportable is explicitly marked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and developers use this skill to compose or rewrite documents that need strict support from provided source material, such as legal, board, regulatory, or enterprise-buyer drafts. The skill produces cited prose, a source map, an unsupported-claims register, and a coverage score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may flag claims as unsourced or remove them from the document when the provided sources are incomplete.

Mitigation: Provide complete source material and choose soft or hard strictness based on whether unsupported claims should remain visible or move to the register.

Risk: A document can look more reliable than it is if cited passages are not checked against the claims they support.

Mitigation: Review the source map and spot-check quoted passages before using the output in legal, regulatory, board, or customer-facing settings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/evidence-lock)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/evidence-lock.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown document with numbered citations, source map, unsupported-claims register, and coverage score]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided sources; supports soft mode with unsourced claims flagged and hard mode with unsupported claims moved to the register.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
