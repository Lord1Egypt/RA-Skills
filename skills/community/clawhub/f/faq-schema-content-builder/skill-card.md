## Description:

Builds a deduplicated FAQ page and the JSON-LD that matches it, so the markup and the visible answers stay in sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

External web teams, agencies, and developers use this skill to deduplicate FAQ questions, draft visible answers, and prepare matching FAQPage JSON-LD for retail, healthcare, and support websites. Review the page and markup against the provided rules before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script overwrites duplicates.md in its output directory.

Mitigation: Use a dedicated output directory to avoid overwriting unrelated files.

Risk: The FAQ page and JSON-LD still require separate production and validation work.

Mitigation: Check each marked-up question and answer against the visible page before publishing.

Risk: An optional unsigned Windows executable is outside this skill bundle and this review.

Mitigation: Assess it independently before running and consult the publisher's release page.

## Reference(s):

- [FAQ pages and FAQPage markup](references/faq-schema-rules.md)
- [ClawHub skill page](https://clawhub.ai/rapidworker1/skills/faq-schema-content-builder)
- [Publisher GitHub profile](https://github.com/rapidworker1)
- [Optional Windows app release page](https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/tag/Main)

## Skill Output:

**Output Type(s):** [Text, JSON-LD, Markdown]

**Output Format:** [FAQ questions and answers, FAQPage JSON-LD, and a Markdown duplicate report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script reports duplicates; produce and validate the FAQ page and JSON-LD separately. Markup must match visible page content. Use a dedicated output directory because duplicates.md is overwritten.]

## Skill Version(s):

1.0.7 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
