## Description:

Clash Auto Switch helps an agent check Clash proxy health, list proxy groups, and switch to a responsive or region-preferred node.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to monitor local Clash proxy connectivity and switch nodes manually, automatically, or by preferred region. It is suited for environments where an agent is allowed to call a local Clash controller.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe credential handling can expose the local Clash controller secret.

Mitigation: Use a unique local Clash secret through environment configuration, keep the controller bound to localhost, and avoid passing secrets on command lines or committing them to config files.

Risk: The bundled shell scripts are flagged for hardcoded secret handling, injectable shell behavior, and temporary state handling.

Mitigation: Prefer the Python skill path and avoid the shell scripts until those issues are fixed.

Risk: Elevated scheduled tasks can increase impact if the skill or local proxy configuration is misused.

Mitigation: Do not run scheduled health checks as administrator or root.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adminlove520/skills/clash-auto-switch)
- [OpenClaw installation guide](docs/openclaw.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include proxy health summaries, proxy group listings, node switch status, and setup guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
