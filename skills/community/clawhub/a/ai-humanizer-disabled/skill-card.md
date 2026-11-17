## Description:

Humanize AI-generated text by detecting common LLM writing patterns, scoring drafts, and suggesting edits that make text sound more natural.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinzorro86](https://clawhub.ai/user/robinzorro86)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, editors, and developers use this skill to analyze drafts for AI-style language, get prioritized findings, and rewrite text or configure agents to produce more natural prose.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autofix rewrites may change nuance, tone, or meaning in a draft.

Mitigation: Review rewritten text before using it, especially for high-stakes or externally published content.

Risk: Always-on prompt snippets can be inappropriate for legal, academic, compliance, evidence, or exact-quotation work.

Mitigation: Keep always-on writing rules scoped to suitable drafting contexts and disable them where exact wording or formal constraints matter.

Risk: Exposing the HTTP API beyond localhost can create abuse or sensitive-draft handling risks.

Mitigation: Add request-size limits, authentication, rate limiting, and clear handling rules for sensitive drafts before network exposure.

## Reference(s):

- [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Copyleaks stylometric research](https://arxiv.org/abs/2503.01659)
- [AI vocabulary reference](references/ai-vocabulary.md)
- [Pattern documentation](references/patterns.md)
- [Real-world before/after examples](docs/EXAMPLES.md)
- [Humanizer integrations](docs/INTEGRATIONS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text, Markdown reports, JSON analysis, command-line examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scores, pattern findings, rewrite suggestions, autofixed text, and statistical indicators such as burstiness, type-token ratio, sentence variation, and repetition.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and package metadata report 2.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
