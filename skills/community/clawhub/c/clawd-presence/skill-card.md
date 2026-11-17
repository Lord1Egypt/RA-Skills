## Description:

Clawd Presence shows a customizable terminal monogram, status state, and current activity so operators can monitor AI agents at a glance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voidcooks](https://clawhub.ai/user/voidcooks)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to run a local terminal display that shows an agent's monogram, current state, and activity message on a dedicated screen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes local configuration and status files in its own directory.

Mitigation: Install it in a location where those files are expected, and review config.json and state.json if local state matters.

Risk: The --auto option may read local clawdbot configuration files to infer an agent name.

Mitigation: Use manual configuration with --letter and --name when local agent configuration should not be read.

Risk: PyYAML may be needed for auto-detection.

Mitigation: Use a virtual environment for any optional dependency installation instead of ad hoc global pip installs.

## Reference(s):

- [Clawd Presence on ClawHub](https://clawhub.ai/voidcooks/skills/clawd-presence)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and local terminal status display output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local config.json and state.json files in the skill directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
