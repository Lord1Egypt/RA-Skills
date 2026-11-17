## Description:

Book Deep Reader researches Chinese or English books and produces teaching-quality Markdown notes with structured summaries, critical evaluation, cross-disciplinary insights, and action guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingluu](https://clawhub.ai/user/kingluu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to research a book from a title, author, ISBN, or URL and generate a structured reading guide that can support learning, teaching, critique, and practical action planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches the web and may rely on secondary book information when original sources are unavailable.

Mitigation: Ask the agent to cite sources, flag unverifiable claims, and avoid unsupported details.

Risk: The skill writes a Markdown notes file in the workspace, and the default filename or language may not match the user's expectations.

Mitigation: State the desired output language, filename, and location before running the skill, and ask the agent not to overwrite existing files.

## Reference(s):

- [Book Deep Reader Skill Page](https://clawhub.ai/kingluu/skills/book-deep-reader)
- [Five-Layer Analysis Framework](references/analysis-framework.md)
- [Output Template](references/output-template.md)
- [Research Methods Reference](references/research-methods.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown file with structured notes, tables, source citations, critical evaluation, and action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a book-specific notes file in the workspace; Chinese books may use a Chinese filename and English books may use an English filename.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
