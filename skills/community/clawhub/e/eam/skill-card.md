## Description:

Enterprise asset management tracker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to track enterprise asset entries from a local command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe input handling in the helper script can allow crafted configuration data to run commands.

Mitigation: Review the script before installing and use only trusted input until the input handling is fixed.

Risk: Remove and export commands persistently change local files, and exports may overwrite files in the current directory.

Mitigation: Avoid storing secrets in configuration, review data before removal, and run exports from a controlled working directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/eam)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes command usage and local JSONL data storage under the configured EAM directory.]

## Skill Version(s):

1.0.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
