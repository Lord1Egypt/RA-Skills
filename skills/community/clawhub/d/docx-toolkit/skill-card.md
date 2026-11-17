## Description:

Extract text, tables, and images from .docx and legacy .doc files. Handles large documents, CJK text, and complex table structures. Includes deduplication and filtering for extracted images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacjiang](https://clawhub.ai/user/zacjiang)

### License/Terms of Use:


## Use Case:

Developers and document-processing teams use this skill to extract text, tables, and embedded images from Word documents for analysis, migration, image review, and batch processing. The skill also helps resize extracted images before downstream vision or review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can introduce supply-chain or environment drift risk.

Mitigation: Install python-docx, olefile, and Pillow in an isolated virtual environment with pinned versions.

Risk: Extracted text, images, and manifests can contain sensitive content copied from the original documents.

Mitigation: Store outputs in controlled directories and apply the same access controls and retention rules used for the source documents.

Risk: The optional image context manifest can save nearby paragraph text alongside extracted images.

Mitigation: Enable --context only when saving surrounding document text into image_manifest.json is acceptable.

Risk: Image resizing can overwrite files when no separate output directory is supplied.

Mitigation: Use explicit output directories, especially for compression or batch processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zacjiang/skills/docx-toolkit)
- [Publisher profile](https://clawhub.ai/user/zacjiang)

## Skill Output:

**Output Type(s):** [text, files, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with bash commands; generated artifacts include UTF-8 text files, extracted image files, and optional JSON manifests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python scripts against user-provided Word documents and image directories.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
