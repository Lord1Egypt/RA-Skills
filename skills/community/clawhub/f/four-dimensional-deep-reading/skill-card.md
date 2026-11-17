## Description:

Four Dimensional Deep Reading analyzes books or uploaded files through four persona perspectives, synthesizing first principles, structured notes, counterarguments, and unexpected viewpoints into multilingual reports with optional exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangboheng](https://clawhub.ai/user/zhangboheng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a book title or document into multi-perspective reading analysis, quick summaries, structured notes, and reusable flashcards or knowledge-base exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic web lookups may disclose book titles, queries, or surrounding context to external services.

Mitigation: Use the skill only with content you are comfortable sending through lookup tools, or disable external lookup behavior before analyzing sensitive material.

Risk: Report and cache persistence may retain analyzed content in the workspace.

Mitigation: Review the generated workspace/reports output and cache locations, and delete retained files when working with private or time-limited material.

Risk: Multi-agent analysis of untrusted content can amplify misleading claims or instructions from source documents.

Mitigation: Review generated analysis before relying on it, especially for sensitive decisions or adversarial documents.

Risk: Notion export can send report content to a configured external workspace.

Mitigation: Configure Notion export only when intentional, and confirm the target database and API credentials before syncing reports.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhangboheng/skills/four-dimensional-deep-reading)
- [Author Website](https://www.luckydesigner.space)
- [Identity Modules](artifact/reference/identity_modules.md)
- [Book Parser Reference](artifact/reference/book_parser.py)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown analysis reports, CSV flashcards, Obsidian Markdown, and Notion JSON blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save reports under workspace/reports and export to external knowledge tools when configured.]

## Skill Version(s):

1.8.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
