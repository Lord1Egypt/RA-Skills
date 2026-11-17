## Description:

Monitors and restarts OpenClaw Gateway around the clock by running an external watchdog process.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adminlove520](https://clawhub.ai/user/adminlove520)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to keep OpenClaw Gateway available by starting a watchdog that checks Gateway status and restarts it after repeated failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can start a persistent local watchdog process that repeatedly checks and restarts Gateway under the user's account.

Mitigation: Install only when continuous Gateway restart behavior is desired, run it without administrator or root privileges, and use the provided stop command when watchdog behavior is no longer needed.

Risk: The one-click installer can download or execute watchdog code and the watchdog can fall back to dependency execution paths such as npx.

Mitigation: Review the bundled gateway_watchdog.py before installation, avoid the one-click installer unless that local file is present and reviewed, and confirm OpenClaw is installed from a trusted source before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adminlove520/skills/gateway-watchdog-xiaoxi)
- [README](artifact/README.md)
- [CHANGELOG](artifact/CHANGELOG.md)
- [SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with command examples and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local watchdog configuration, log, and PID files when the generated commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata and changelog, released 2026-03-03)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
