## Description:

Localizes English board-game rulebook PDFs into Chinese while preserving the original layout, with a board-game glossary, table and inline-icon handling, and automated QA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c0s1n3](https://clawhub.ai/user/c0s1n3)

### License/Terms of Use:

MIT

## Use Case:

External users can translate English board-game rulebook PDFs into Chinese while preserving page layout, illustrations, tables, and inline icons. It is intended for PDFs with selectable text; scanned or image-only pages need a different workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup can permanently delete existing files without warning.

Mitigation: Use fresh, dedicated output and self-test directories, keep backups, and avoid reusing existing QA or self-test folders until ownership checks and overwrite protection are in place.

## Reference(s):

- [Project repository](https://github.com/C0S1N3/boardgame-rulebook-zh)
- [ClawHub skill page](https://clawhub.ai/C0S1N3/skills/boardgame-rulebook-zh)

## Skill Output:

**Output Type(s):** [Files, PDF documents, Markdown reports, PNG previews, TSV terminology data]

**Output Format:** [Localized PDF, Markdown QA report, PNG page previews, and TSV termbase]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [QA errors must be resolved before delivery; warnings require review.]

## Skill Version(s):

1.0.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
