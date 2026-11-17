## Description:

A Chinese-language compliance archive skill for managing enterprise legal documents and policies through document archiving, version updates, obsolete-version marking, search, and file-list export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Compliance, legal, and operations teams use this skill to organize policy documents, record version history, locate archived materials, and export document inventories from a local archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports serious input-handling flaws that could corrupt archive records or write files outside the intended archive directory.

Mitigation: Review the script before installation and parameterize SQL inputs, allowlist document types to fixed directories, prevent overwrites, and tighten archive permissions before using important compliance files.

Risk: Obsolete-version changes can affect compliance records.

Mitigation: Require an explicit preview and confirmation before marking older document versions obsolete.

## Reference(s):

- [File Classification](artifact/references/file-classification.md)
- [Version Control](artifact/references/version-control.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local archive status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce archive identifiers, archive paths, version-change summaries, search results, and exported document inventory records.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
