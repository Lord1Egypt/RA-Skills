## Description: <br>
Monitors and restarts OpenClaw Gateway by running an external watchdog process for continuous operation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who run OpenClaw Gateway use this skill to start a watchdog process, check gateway status, and restart the gateway after repeated failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The one-click path can run a persistent background watchdog process. <br>
Mitigation: Install only when continuous OpenClaw Gateway monitoring is desired, run it with least privileges, and use the documented stop command when monitoring is no longer needed. <br>
Risk: The installer includes an unpinned remote download-and-execute fallback. <br>
Mitigation: Prefer reviewing and running the bundled gateway_watchdog.py directly instead of relying on install.py's remote download fallback. <br>
Risk: Generated configuration and PID files can affect process control, especially on Windows. <br>
Mitigation: Protect the generated config and PID files and avoid sharing writable access to the skill directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adminlove520/gateway-watchdog-xiaoxi) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/adminlove520) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact CHANGELOG](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command-output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The included scripts may create local configuration, log, and PID files when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact CHANGELOG, released 2026-03-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
