## Description:

Generate polished .docx documents by injecting Markdown content into an existing Word template while preserving the template's cover page, TOC, fonts, headers, and footers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loki612](https://clawhub.ai/user/loki612)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and enterprise document authors use this skill to turn a Word template plus reference materials into a production-ready .docx deliverable with traceable research notes, per-chapter Markdown drafts, rendered Mermaid diagrams, and template-preserving injection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Mermaid rendering step can invoke unpinned external tooling through npx.

Mitigation: Pin or preinstall the Mermaid CLI version before using the skill, especially for confidential or regulated documents.

Risk: The included Mermaid renderer uses Chromium with sandboxing disabled for Linux/container compatibility.

Mitigation: Run the skill in an isolated workspace or container with no sensitive environment variables and only the document files needed for the task.

Risk: The skill processes local templates and reference files that may contain confidential corporate information.

Mitigation: Use copies of templates and reference materials, restrict the source-material whitelist, and review generated research notes and drafts before final injection.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loki612/skills/corporate-doc-builder)
- [Publisher profile](https://clawhub.ai/user/loki612)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and generated document assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged research notes, chapter Markdown files, rendered Mermaid PNGs, and a final .docx document when the included scripts are run.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
