## Description:

Book Organizer helps users create structured Markdown notes for books, including summaries, chapter outlines, mind maps, concepts, key quotes, core ideas, reflections, and reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ioygy](https://clawhub.ai/user/ioygy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to organize book information and reading material into structured Markdown notes, including summaries, concepts, quotations, mind maps, and review sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill directs agents to retrieve full ebooks from questionable external libraries and search for PDFs or downloads before summarizing them.

Mitigation: Constrain use to user-provided, licensed, or public-domain material and avoid retrieving copyrighted full-text books from unauthorized sources.

Risk: The security guidance notes that the skill saves generated notes locally.

Mitigation: Confirm intended file paths before writing and review generated Markdown before relying on it.

## Reference(s):

- [Book organization output templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown files with structured sections, tables, quotes, and optional Mermaid mind maps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated notes to the workspace root or a books folder.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
