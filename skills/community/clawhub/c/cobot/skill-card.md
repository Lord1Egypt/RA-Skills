## Description:

Cobot provides CLI commands for recording, listing, searching, exporting, and configuring local cobot task entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators can use this skill for CLI-based local tracking of cobot-related entries, status checks, search, export, statistics, and simple configuration. It should be treated as a local note/configuration helper rather than a robot planner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because the skill claims collaborative robot task planning while the inspected artifact behaves as a local entry and configuration manager.

Mitigation: Review the artifact before installation and treat it as a local note/configuration CLI, not as a robot planner.

Risk: The bundled script persists entries and configuration under COBOT_DIR and can export local data to JSON or CSV files.

Mitigation: Keep COBOT_DIR in a private directory you control and avoid storing sensitive information in entries or exported files.

Risk: Unsafe input handling and CSV export can preserve untrusted values in local files.

Mitigation: Do not pass untrusted values to add, search, or config commands, and avoid opening exported CSVs from untrusted entries in spreadsheet software.

## Reference(s):

- [Cobot on ClawHub](https://clawhub.ai/ckchzh/skills/cobot)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and plain text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local JSONL data, CSV exports, JSON exports, and configuration files when the bundled shell script is executed.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
