## Description:

File Splitter splits large JSON, Markdown, and TXT files into smaller chunks at semantic boundaries while preserving source files and data integrity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[expeditionhub](https://clawhub.ai/user/expeditionhub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data practitioners, and external users use this skill to split large files, chunk datasets, segment corpora, or prepare JSON, Markdown, and text files for processing and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Predictable chunk filenames can replace existing files in an unsafe or shared output folder.

Mitigation: Use a new or trusted output folder, run dry-run first, and avoid attacker-writable output directories.

## Reference(s):

- [File Splitter Skill Page](https://clawhub.ai/expeditionhub/skills/file-splitter)
- [ExpeditionHub Publisher Profile](https://clawhub.ai/user/expeditionhub)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated chunk files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces sequentially named JSON, Markdown, or TXT chunk files in a user-selected output folder; supports dry-run preview.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
