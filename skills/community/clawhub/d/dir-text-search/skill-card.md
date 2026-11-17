## Description:

Searches for text or regular expression patterns inside a directory, including recursively inside ZIP, RAR, TAR, and 7z archives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trylovecatch](https://clawhub.ai/user/trylovecatch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to locate strings or regular expression matches across local project files, logs, configuration files, and supported compressed archives. It helps summarize matching files and lines while saving detailed results to local output files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanning untrusted archive collections can create local safety risks during extraction.

Mitigation: Run searches on untrusted archives in a restricted environment with storage limits.

Risk: Matching content is saved to local result files and may include sensitive text from searched files.

Mitigation: Choose an appropriate output directory and review or delete result files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/trylovecatch/skills/dir-text-search)
- [RARLab UnRAR download](https://www.rarlab.com/rar_add.htm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown summary with shell commands and local text result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped search result files under search_results/ or a user-specified output directory.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
