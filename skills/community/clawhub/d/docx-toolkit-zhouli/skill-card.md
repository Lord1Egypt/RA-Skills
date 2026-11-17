## Description:

Extract text, tables, and images from .docx and legacy .doc files. Handles large documents, CJK text, and complex table structures. Includes deduplication and filtering for extracted images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to extract Word document text, tables, embedded images, and resized image assets for analysis, migration, audit, and batch-processing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local document-processing tools operate on user-selected Word files and third-party Python dependencies.

Mitigation: Install in a virtual environment, consider pinning dependency versions, and run the tools only on documents you intend to process.

Risk: Image resizing can overwrite originals and lossy compression may change image quality or format when no output directory is supplied.

Mitigation: Use explicit output directories for resizing workflows and retain source images when preserving originals matters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/skills/docx-toolkit-zhouli)
- [Publisher Profile](https://clawhub.ai/user/onlyloveher)
- [Skill YAML Homepage](https://clawhub.com/skills/docx-toolkit)

## Skill Output:

**Output Type(s):** [Text, Files, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include text or TSV content, image files, and an optional JSON image manifest.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local file-processing outputs; image resizing can overwrite originals when no output directory is provided.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, evidence.release.version, _meta.json, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
