## Description:

Configure and maintain ClawPulse integration for OpenClaw, including a token-protected status bridge, Tailscale-safe access, iOS endpoint/token defaults, and troubleshooting for ATS, auth, and sync issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[virtual-ny](https://clawhub.ai/user/virtual-ny)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up and maintain an OpenClaw status bridge for ClawPulse, including bridge and monitor setup, token rotation, app endpoint configuration, and connectivity troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bridge and monitor can expose assistant status over a network service.

Mitigation: Run only on machines and networks where exposing assistant status is acceptable; prefer 127.0.0.1 or a tightly controlled Tailscale interface.

Risk: Printed bearer tokens and QR setup codes grant access to the status endpoint.

Mitigation: Treat printed tokens and QR codes as secrets, rotate tokens when needed, and update ClawPulse immediately after rotation.

Risk: Background bridge and monitor processes may continue exposing status after setup.

Mitigation: Stop or remove the background processes when ClawPulse access is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/virtual-ny/skills/clawpulse-bridge)
- [Publisher Profile](https://clawhub.ai/user/virtual-ny)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, generated configuration values, setup links, QR-code artifacts, and JSON status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local bridge and monitor scripts, local environment files containing bearer tokens, logs, and ClawPulse setup QR images.]

## Skill Version(s):

2.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
