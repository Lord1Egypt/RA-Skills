## Description:

Print files uploaded to a Feishu group chat with smart matching for multiple files, filename prefix or keyword filters, file type, and time range, and support direct text printing and printer queue commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caigang78](https://clawhub.ai/user/caigang78)

### License/Terms of Use:


## Use Case:

External users and operators use this skill to print files from a Feishu group chat by recency, name, type, or time range. They can also print direct text content and inspect or manage printer queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on Feishu downloader components outside the reviewed package.

Mitigation: Install only trusted shared downloader components from a known source before using the skill.

Risk: Broad printer-management commands can affect other print jobs.

Mitigation: Use the skill in a controlled single-user printer setup and avoid blanket cancellation commands.

Risk: Downloaded or temporary files may remain on disk after printing.

Mitigation: Prefer a version that limits printer management and cleans up downloaded or temporary files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and environment-variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured printer and trusted Feishu downloader components.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
