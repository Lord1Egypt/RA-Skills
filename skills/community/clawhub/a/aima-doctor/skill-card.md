## Description:

Diagnose and repair OpenClaw when your agent is stuck, confused, or failing. One-command rescue for process health, config breakage, and device registration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skyguan92](https://clawhub.ai/user/skyguan92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to diagnose degraded or failed OpenClaw sessions, repair process and configuration problems, recover AIMA device registration, and run guided local repairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs a separate AIMA Doctor runtime that is not included in the reviewed artifact.

Mitigation: Review or explicitly trust the separate runtime before use, verify the documented SHA256 checksum, and prefer running it in a restricted environment.

Risk: The helper may run with the user's account access to OpenClaw files, processes, and recovery material.

Mitigation: Avoid sharing sensitive tokens or recovery codes unless the repair specifically requires them, and keep sensitive material out of normal chat.

## Reference(s):

- [AIMA Doctor homepage](https://aimaservice.ai/doctor)
- [AIMA OpenClaw repository](https://github.com/Approaching-AI/aima-openclaw)
- [AIMA OpenClaw releases](https://github.com/Approaching-AI/aima-openclaw/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download and invoke a separate local AIMA Doctor runtime after checksum verification.]

## Skill Version(s):

0.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
