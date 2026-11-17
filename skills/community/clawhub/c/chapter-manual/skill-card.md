## Description:

Manages chapter handbooks by organizing large sets of source files into a structured multi-file manual, supporting directory and content edits, handbook-based Q&A, and incremental updates from new material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orionzou](https://clawhub.ai/user/orionzou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn scattered Markdown files and links into a structured, maintainable handbook with a table of contents, chapter files, source notes, and internal links. It also supports maintaining an existing handbook through edits, reorganization, Q&A, and incremental updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read every Markdown file in a selected directory and incorporate source material into generated handbook files.

Mitigation: Run it only on directories and URLs the user intends the assistant to read, and review generated handbook content before sharing.

Risk: Source material can be summarized, reorganized, or merged into new handbook sections, which may introduce omissions or misplacements.

Mitigation: Review the proposed table of contents and updated sections, and preserve or correct source notes for important claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/orionzou/skills/chapter-manual)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown handbook files with table of contents, internal links, and source notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or update multi-file handbook directories, including README.md, TOC.md, chapter index files, section files, and assets references.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
