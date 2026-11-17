## Description:

Builds per-chapter H2 writing briefs so survey chapters have stronger lead plans and cross-H3 coherence without expanding the table of contents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[willoscar](https://clawhub.ai/user/willoscar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and writing agents use this skill after an outline and subsection briefs exist to create chapter-level JSONL planning records for survey-style writing. The records help plan chapter leads, comparison axes, synthesis mode, key contrasts, and stable bridge terms without generating reader-facing prose or inventing citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom input or output paths may read or write files outside the intended chapter brief workflow.

Mitigation: Use the documented default paths or enforce an allowlist limited to outline/outline.yml, outline/subsection_briefs.jsonl, GOAL.md, and outline/chapter_briefs.jsonl.

Risk: The package includes broad pipeline tooling beyond the chapter-brief helper.

Mitigation: Review the bundled files before installation and run the helper in a contained workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/willoscar/skills/chapter-briefs)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions plus JSONL records in outline/chapter_briefs.jsonl]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 or python; default inputs are outline/outline.yml, outline/subsection_briefs.jsonl, and optional GOAL.md.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
