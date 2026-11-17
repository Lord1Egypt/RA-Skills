## Description:

CNC machining program manager.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and CNC operators can use this skill to run a small Bash CLI for recording, listing, searching, removing, exporting, and configuring local CNC-related entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill is mislabeled as a CNC manager while behaving as a local data tracker.

Mitigation: Review the script behavior before installation and treat it as a local note tracker unless CNC-specific functionality is independently verified.

Risk: Unsafe input handling may corrupt stored data or allow command execution through crafted config values.

Mitigation: Do not pass untrusted text to add or config commands; require input validation and proper JSON/CSV encoding before operational use.

Risk: The script creates and modifies local files, deletes entries, and writes export files in the current directory.

Mitigation: Run with an isolated CNC_DIR, back up data before using remove, and inspect export output paths before execution.

## Reference(s):

- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Markdown command guidance and structured stdout from a Bash CLI; local JSONL, JSON, and CSV files may be written.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CNC_DIR when set; otherwise stores data under ~/.cnc/ and may write cnc-export.json or cnc-export.csv in the current directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
