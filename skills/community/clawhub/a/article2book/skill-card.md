## Description:

Article2Book helps an agent assess existing articles, columns, course scripts, transcripts, interviews, notes, PDF text, Word documents, and related content assets, then recommend whether they should become a book, booklet, course, article series, practice manual, knowledge base, or remain unproductized.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cat-xierluo](https://clawhub.ai/user/cat-xierluo)

### License/Terms of Use:

MIT

## Use Case:

External users, authors, consultants, and content strategists use this skill to evaluate a directory of existing text-based content assets and turn them into a concise productization plan. It supports staged delivery: first a planning recommendation, then an optional draft for the recommended content form after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may read sensitive or mixed-trust documents from the selected content directory.

Mitigation: Use a narrow source folder, remove unrelated private materials, and review generated recommendations before sharing or publishing them.

Risk: Generated CSV inventory files may be unsafe to open directly in spreadsheet software if source filenames or metadata contain formula-like text.

Mitigation: Sanitize formula-like cells or inspect the inventory in a plain-text editor before opening it in a spreadsheet application.

Risk: Content productization recommendations can be incomplete or misleading if the source set is stale, repetitive, or not fully text-readable.

Mitigation: Confirm the source set, require human review of the planning recommendation, and preprocess PDF, Word, audio, video, or scanned materials before relying on the result.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cat-xierluo/skills/article2book)
- [Project Homepage](https://github.com/cat-xierluo/legal-skills)
- [Agent Reading Protocol](references/agent-reading-protocol.md)
- [Book Viability Rubric](references/book-viability-rubric.md)
- [Content Productization Models](references/content-productization-models.md)
- [Content Screening Rubric](references/content-screening-rubric.md)
- [Output Template](references/output-template.md)
- [Source Type Handling](references/source-type-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown planning files with optional CSV, JSONL, and Markdown inventory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to a single planning recommendation under the source directory; optional inventory artifacts are generated only when useful or requested.]

## Skill Version(s):

1.0.0 (source: frontmatter and changelog, released 2026-05-17)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
