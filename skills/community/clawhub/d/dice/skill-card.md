## Description:

Dice is a local command-line tabletop gaming logger for recording game notes, reviewing logged activity, and exporting history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

External tabletop gaming users can use this skill to keep local game-themed logs, inspect recent entries, search history, and export logged data. It should not be relied on as an actual dice roller or score calculator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may expect real dice rolling or score calculation from the skill name and summary.

Mitigation: Present and use it as a local logging and export utility, and verify game outcomes or scores with a separate trusted tool.

Risk: Local logs and exports may contain sensitive player or session information.

Mitigation: Avoid entering sensitive information and review exported files before sharing or storing them outside the local machine.

Risk: JSON and CSV exports can be unsafe or malformed when entries contain quotes, commas, newlines, or spreadsheet formula characters.

Mitigation: Treat exported files as untrusted, inspect them before import, and avoid opening CSV exports directly in spreadsheet software when entries come from untrusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/dice)
- [Publisher profile](https://clawhub.ai/user/bytesagain3)
- [Publisher homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Configuration]

**Output Format:** [Command-line text with local log files and optional JSON, CSV, or TXT exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores entries locally under ~/.local/share/dice/.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
