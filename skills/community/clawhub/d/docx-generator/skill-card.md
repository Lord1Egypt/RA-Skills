## Description:

Creates Microsoft Word (.docx) documents with an AI-generated-content footer, supporting titles, paragraphs, lists, tables, code blocks, images, and links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[983488728](https://clawhub.ai/user/983488728)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create Word documents, reports, and formatted text exports that can include structured content and an AI disclaimer footer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create directories and write DOCX files at paths requested by the user.

Mitigation: Review output paths before execution and run the skill with workspace-scoped file permissions where possible.

Risk: The skill can embed image files provided by path.

Mitigation: Use only intended local images and avoid embedding sensitive files into generated documents.

Risk: Generated documents default to a Chinese AI-disclaimer footer that may not fit every audience or policy.

Mitigation: Confirm or customize the footer text before distributing generated documents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/983488728/skills/docx-generator)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands, Guidance]

**Output Format:** [DOCX files plus Markdown guidance with Python or shell code blocks when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents are saved to user-requested .docx paths and include a configurable footer that defaults to Chinese AI-disclaimer text.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact files mention 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
