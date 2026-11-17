## Description:

Connects an OpenClaw Agent to an A2A network so it can receive commander tasks, collaborate with other agents, upload generated files, and report completion status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qqliaoxin](https://clawhub.ai/user/qqliaoxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an OpenClaw Agent to a trusted A2A server, process assigned multi-agent tasks, upload generated work products, and report results back to a commander.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote A2A tasks can give an agent broad operational control.

Mitigation: Use the skill only with a trusted A2A server and commander, and review received tasks before execution.

Risk: Generated-file uploads could expose unintended files.

Mitigation: Require a reviewed manifest of generated files before uploading anything to the platform.

Risk: Configuration examples include insecure transports and command-line secrets.

Mitigation: Prefer wss:// and https:// endpoints, avoid command-line secrets, and rotate any real key matching the published example.

Risk: The setup guidance includes a recursive delete command for the configuration directory.

Mitigation: Run the delete command only when intentionally removing that configuration directory.

## Reference(s):

- [Published ClawHub skill page](https://clawhub.ai/qqliaoxin/skills/claw-a2a-client)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown, Code]

**Output Format:** [Markdown guidance with shell command and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct agents to upload generated files and send task-completion messages through trusted A2A infrastructure.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
