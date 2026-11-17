## Description:

Build Word literature reviews from BibTeX, RIS, CSL JSON, CSV/TSV, or plain reference lists with GB/T 7714, APA, MLA, Chicago, IEEE, Vancouver, or Harvard bibliography formatting and clickable Word REF citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephenlzc](https://clawhub.ai/user/stephenlzc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writing agents use this skill to turn curated literature sources into Chinese or English Word literature reviews with structured citations, bibliography formatting, and DOCX cross-reference validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes an unrelated agent memory-context block.

Mitigation: Remove the AGENTS.md memory-context block before installation, or confirm the target agent will not load it.

Risk: DOCX validation processes local document archives without evidence of archive size or file-count limits.

Mitigation: Run the validator only on trusted DOCX files until archive limits are added.

Risk: Bibliography formatting and metadata normalization may not satisfy strict publication or institution-specific requirements without review.

Mitigation: Manually review final bibliography punctuation, capitalization, proper nouns, missing fields, and institution-specific formatting before delivery.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/stephenlzc/skills/bibtex-literature-review)
- [Workflow](references/workflow.md)
- [Supported Input Formats](references/input-formats.md)
- [Citation and Bibliography Styles](references/citation-styles.md)
- [GB/T 7714 from BibTeX](references/gbt7714-bibtex.md)
- [Review JSON Specification](references/review-json-spec.md)
- [Word REF Fields and Bibliography Numbering](references/ooxml-ref-fields.md)
- [Acceptance Criteria](references/acceptance.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands, JSON review data, and generated DOCX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Word REF citations, superscript numeric citation markers, automatic numbered bibliography paragraphs, and validation results.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
