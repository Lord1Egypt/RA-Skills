## Description:

All-in-one deep-reading workflow that turns books, long-form articles, research reports, and papers into a connected Zettelkasten knowledge network with structure, index, atomic, method, and review notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikonos](https://clawhub.ai/user/mikonos)

### License/Terms of Use:


## Use Case:

External users and knowledge workers use this skill to deeply digest books, long articles, research reports, or papers and turn them into a connected Zettelkasten note network rather than a standalone summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can create folders, append to existing indexes, and move notes in a user's note vault.

Mitigation: Run with filesystem access limited to the intended vault and request a preview before file creation, index updates, or note moves.

Risk: The workflow may call companion skills that are not included in this artifact.

Mitigation: Install companion skills only from trusted sources and review them before allowing this workflow to call them.

## Reference(s):

- [Expert Personas](references/expert_personas.md)
- [Luhmann Scan Workflow](references/luhmann_scan.md)
- [Structure Note Template](templates/structure_note_template.md)
- [Atomic Note Template](templates/atomic_note_template.md)
- [Index Note Template](templates/index_note_template.md)
- [Method Note Template](templates/method_note_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files with YAML frontmatter, wiki links, task checklists, and structured note templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a multi-step reading plan and note set; may create directories, append to indexes, and move notes within the user's note vault.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
