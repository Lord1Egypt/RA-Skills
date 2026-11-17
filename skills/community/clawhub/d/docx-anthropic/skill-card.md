## Description:

Helps agents create, read, edit, validate, convert, and manipulate Word .docx documents, including formatting, comments, images, and tracked changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Proprietary Anthropic Terms

## Use Case:

Developers, document automation users, and agent operators use this skill to produce polished Word documents and inspect or modify existing .docx files. It is suited for workflows involving document generation, XML-level repair, comments, tracked changes, validation, and format conversion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document-processing paths may execute LibreOffice with unsafe profile or shim behavior and unpinned global dependencies.

Mitigation: Run the skill in an isolated environment, avoid untrusted Office files until the flagged issues are fixed, and prefer pinned local dependencies over global installs.

Risk: Comments and tracked changes can expose default author names in shared documents.

Mitigation: Set explicit comment and tracked-change author names before producing documents for others.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pupuking723/skills/docx-anthropic)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with code and shell command examples; generated artifacts may include .docx files and unpacked Office XML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke local document tooling such as LibreOffice, pandoc, docx-js, and Python helper scripts when those tools are available.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
