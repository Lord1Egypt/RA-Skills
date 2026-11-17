## Description:

Fast and comprehensive Windows file and folder search using the Everything command line tool with filters, sorting, and CSV export options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thianda91](https://clawhub.ai/user/thianda91)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Windows users use this skill to construct Everything CLI searches for locating files and folders, filtering and sorting results, troubleshooting es.exe compatibility, and exporting results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help enumerate broad areas of a Windows filesystem.

Mitigation: Review generated commands before execution and scope searches to approved folders instead of broad roots such as C:\.

Risk: CSV exports can create sensitive inventories of local files.

Mitigation: Store exports deliberately, restrict access to them, and delete them when they are no longer needed.

Risk: The artifact includes installation guidance that suggests copying es.exe into the Windows system directory.

Mitigation: Prefer the official Everything installer or add the verified es.exe directory to PATH; avoid copying binaries into C:\Windows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thianda91/skills/es-file-search-win)
- [Everything downloads](https://www.voidtools.com/downloads/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Windows command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Everything CLI commands, setup checks, filters, sorting options, and CSV export guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
