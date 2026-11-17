## Description:

Get the physical location of your macOS device and print it to stdout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerrykfc](https://clawhub.ai/user/jerrykfc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run CoreLocationCLI on macOS and retrieve the current device location as plain text, formatted text, or JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose precise device location, coordinates, or address data in terminal output, logs, transcripts, demos, or automation.

Mitigation: Install and run it only when location access is intended; avoid shared logs and transcripts, and use --json or --watch only where sensitive output is controlled.

Risk: The CLI may fail or be blocked in unsupported or unapproved macOS environments.

Mitigation: Confirm macOS support, Wi-Fi availability, swift availability, and first-run Gatekeeper approval before relying on location output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerrykfc/skills/corelocationcli)
- [Publisher profile](https://clawhub.ai/user/jerrykfc)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with CLI usage examples and optional plain-text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS and the swift binary; location output may include coordinates and reverse-geocoded address data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
