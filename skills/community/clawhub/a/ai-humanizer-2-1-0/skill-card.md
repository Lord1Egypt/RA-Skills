## Description:

Detects common AI-writing patterns, scores text with heuristic and statistical signals, and suggests edits that make drafts sound more natural and specific.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hades4501](https://clawhub.ai/user/hades4501)

### License/Terms of Use:

MIT

## Use Case:

Writers, editors, and agent builders use this skill to analyze drafts for AI-like phrasing, repetitive structure, and generic style, then apply targeted suggestions or safe mechanical fixes while preserving the draft's meaning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heuristic AI-writing scores may be mistaken for proof of authorship.

Mitigation: Treat scores and labels as editing signals only, and do not use them as evidence that a person or AI wrote a text.

Risk: Humanizing suggestions can be used to misrepresent authorship, identity, or personal experience.

Mitigation: Use suggestions for clarity and style edits, and keep authorship, sourcing, and personal-experience claims honest.

Risk: Developer tooling relies on npm development dependencies.

Mitigation: Pin and audit development dependencies before running lint, test, or formatting workflows in a trusted environment.

## Reference(s):

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659)
- [Pattern documentation](docs/PATTERNS.md)
- [Examples](docs/EXAMPLES.md)
- [Pattern reference](references/patterns.md)
- [AI vocabulary reference](references/ai-vocabulary.md)
- [Style guide](references/style-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Plain text, Markdown reports, JSON analysis, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can emit scores, pattern findings, statistical metrics, prioritized suggestions, and optional safe autofix text.]

## Skill Version(s):

1.0.0 (source: server release metadata); package version 2.1.0 (source: artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
