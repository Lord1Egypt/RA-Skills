## Description:

Game Dev Assistant helps agents support game data analysis, level and configuration work, asset organization, project build automation, testing, save parsing, engine project assistance, shader debugging, and log analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaochunz030-spec](https://clawhub.ai/user/xiaochunz030-spec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game teams use this skill to ask an agent for help parsing game data, preparing level or configuration files, automating Unity builds, analyzing logs, and producing reports or scripts for game projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide local project reads and writes, save edits, and Unity builds that may affect project files or create build outputs.

Mitigation: Confirm target paths and requested actions before editing saves, changing versioned files, running builds, signing, or uploading outputs.

Risk: CSV exports from untrusted game data can be risky when opened in spreadsheet software.

Mitigation: Review or sanitize exported CSV content before opening it in spreadsheet tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaochunz030-spec/skills/game-dev-assistant)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell commands, JSON, CSV, or configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct scripts that read local project files, write reports, export CSV, or run Unity command-line builds when the user permits.]

## Skill Version(s):

1.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
