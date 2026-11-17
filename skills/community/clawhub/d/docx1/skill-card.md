## Description:

Docx helps agents create, read, edit, convert, validate, and review Microsoft Word .docx documents, including formatted documents, tracked changes, comments, images, and Office XML workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangxiaoqiang1992](https://clawhub.ai/user/yangxiaoqiang1992)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and document-focused agent users use this skill to generate polished Word documents, inspect existing .docx content, apply edits, manage tracked changes and comments, and validate Office XML packaging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run LibreOffice, execute a macro to accept tracked changes, and compile or load a native compatibility shim.

Mitigation: Run the skill in an isolated environment, review these workflows before installation, and address the /tmp shim and LibreOffice profile behavior before shared-system use.

Risk: The skill modifies Office XML and processes Office documents that may be sensitive or untrusted.

Mitigation: Work on copies, avoid sensitive or untrusted Office files unless the environment is isolated, and validate generated documents before distribution.

Risk: The documented setup uses global npm dependency installation for docx-js.

Mitigation: Pin dependencies locally in the project environment instead of relying on global npm installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangxiaoqiang1992/skills/docx1)
- [Publisher profile](https://clawhub.ai/user/yangxiaoqiang1992)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with code and shell command snippets; document workflows may produce .docx, PDF, image, or unpacked XML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires external document tooling such as docx-js, pandoc, LibreOffice, and Office XML validation utilities for some workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
