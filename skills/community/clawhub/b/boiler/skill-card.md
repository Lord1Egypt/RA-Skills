## Description:

Boiler efficiency and sizing tool

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators can use this skill to run a boiler-labeled local CLI for status, entry management, search, export, statistics, and configuration. Security evidence notes it behaves like a persistent local record manager rather than a boiler efficiency or sizing calculator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is branded as a boiler efficiency and sizing tool, but security evidence says it behaves like a persistent local record manager.

Mitigation: Install only when a local generic record manager is intended, and review the skill behavior before using it for boiler-related decisions.

Risk: Stored entries and exports are persistent local files.

Mitigation: Treat BOILER_DIR or ~/.boiler/ and generated exports as local records that may need retention, access, and cleanup controls.

Risk: CSV exports may be unsafe when populated with untrusted data and opened in spreadsheet software.

Mitigation: Avoid opening CSV exports from untrusted data in spreadsheets.

Risk: Security guidance warns against untrusted users or agents passing arbitrary config arguments to the script.

Mitigation: Restrict who can invoke config commands and review config key/value arguments before execution.

## Reference(s):

- [Boiler on ClawHub](https://clawhub.ai/bytesagain3/skills/boiler)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Plain text CLI output, JSONL records, and JSON or CSV exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persistent local data under BOILER_DIR or ~/.boiler/ and can export boiler-export.json or boiler-export.csv.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
