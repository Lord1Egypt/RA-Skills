## Description:

Create professional Word (.docx) documents from a user-provided content list with styled headings, paragraphs, colors, alignment, and formatting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sereinzhi](https://clawhub.ai/user/sereinzhi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert user-provided outlines, reports, letters, summaries, and other structured content into formatted Word documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper automatically installs an unpinned python-docx package when the dependency is missing.

Mitigation: Run it in an environment where automatic package installation is acceptable, or preinstall a pinned python-docx version and review dependency changes.

Risk: The helper can write .docx output to caller-chosen file paths.

Mitigation: Use a dedicated output directory and avoid sensitive, absolute, or arbitrary filenames unless reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sereinzhi/skills/generate-word-docx)

## Skill Output:

**Output Type(s):** [Files, Code, Shell commands]

**Output Format:** [Word (.docx) document with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a .docx file from a list of paragraph objects with optional style, alignment, bold, and color fields.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
