## Description:

Work with PDF files including merge, split, extract text, and convert.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agent users use this skill to inspect and manipulate local PDF files, including extracting text, merging files, splitting documents, extracting pages, and viewing PDF metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool depends on pypdf, so behavior and security depend on the installed package version.

Mitigation: Install in a low-privilege Python environment and use a pinned, reviewed pypdf version.

Risk: The documentation advertises image extraction, conversion, and compression, but the artifact primarily implements local PDF text extraction, merge, split, page extraction, and info operations.

Mitigation: Rely only on the implemented PDF operations unless the package is updated and re-reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/dinghaibin-pdf-tool)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and local file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local PDF or text files when output paths are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
