## Description:

Azuredatastudio provides a local Bash-based command interface for querying, importing, exporting, transforming, validating, and summarizing flat-file data records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data practitioners can use this skill to run lightweight local data-management commands without a database server. It is most appropriate for simple flat-file workflows where command output to stdout or generated files is sufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is marketed like Azure Data Studio but the security evidence describes it as a local demo or stub CLI rather than Microsoft-backed functionality.

Mitigation: Confirm this is the intended package before installation and do not rely on it as a replacement for the official Azure Data Studio application.

Risk: Command history is saved under the configured Azuredatastudio data directory and may include user-provided command arguments.

Mitigation: Avoid passing secrets or sensitive SQL as command arguments, choose an appropriate data directory, and review or clear local history files when needed.

Risk: The scripts create and write local files in the default or configured data directory.

Mitigation: Set AZUREDATASTUDIO_DIR to a controlled location before running the skill when file placement or cleanup matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/azuredatastudio)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and stdout-oriented shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local data and history files under the configured Azuredatastudio data directory.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
