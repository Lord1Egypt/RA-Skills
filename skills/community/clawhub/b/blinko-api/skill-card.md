## Description:

Manage Blinko notes and blinkos from the command line. Use when you need to list, create, update, delete, or promote blinkos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pigd0g](https://clawhub.ai/user/pigd0g)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage Blinko notes and quick blinkos from an agent session or command line, including listing, reading, creating, updating, deleting, and promoting entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive Blinko note content or API credentials could be exposed if the host or token is configured carelessly.

Mitigation: Use a local or HTTPS-only BLINKO_HOST, pass the token through the environment, and prefer a least-privilege token where Blinko supports it.

Risk: Delete commands can remove notes or blinkos and the skill evidence does not show a strong confirmation boundary.

Mitigation: Require explicit user confirmation and verify target IDs before running delete-note or delete-blinko commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pigd0g/skills/blinko-api)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and command output as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads Blinko host and token settings from environment variables or command-line options.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
