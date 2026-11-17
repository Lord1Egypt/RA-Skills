## Description:

Docx helps agents create, read, edit, validate, convert, and manipulate Microsoft Word .docx documents, including formatting, images, comments, and tracked changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zda2019](https://clawhub.ai/user/zda2019)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and document-production agents use this skill to build polished Word documents, inspect or transform existing .docx files, and manage comments or tracked changes with supporting validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Processing untrusted Office files and running LibreOffice automation can expose shared machines to unsafe document behavior.

Mitigation: Review the skill before installation, process untrusted files in an isolated container, and use safer conversion settings.

Risk: The LibreOffice workflow uses a fixed /tmp profile and an LD_PRELOAD socket shim that may be inappropriate for shared environments.

Mitigation: Replace the fixed profile and shim with private per-run temporary directories or approved conversion settings before shared use.

Risk: The release is presented as a DOCX skill, while supporting scripts also handle PPTX and XLSX containers.

Mitigation: Restrict usage to DOCX when that is the intended deployment scope, or review the broader Office-file handling before enabling it.

Risk: Document generation depends on external command-line tools and npm packages.

Mitigation: Pin and locally install required dependencies before deployment, then validate generated documents before delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zda2019/skills/docx-2)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with code blocks and generated or modified Office document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on pandoc, LibreOffice, Poppler, and the npm docx package; validates and repackages Office ZIP/XML files.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
