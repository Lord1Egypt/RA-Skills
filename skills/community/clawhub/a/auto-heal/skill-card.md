## Description: <br>
Auto-Heal monitors OpenClaw gateway status, agent sessions, and memory usage and can automatically restart or clean up unhealthy components. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zacharyzax](https://clawhub.ai/user/zacharyzax) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to run scheduled or continuous health checks, automatically restart the gateway, clean up stuck sessions, and record status when OpenClaw becomes unresponsive or resource constrained. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog can automatically restart OpenClaw services, kill sessions, delete logs, and modify OpenClaw configuration. <br>
Mitigation: Review the scripts and configuration before enabling unattended cron or continuous monitoring, and test with manual checks first. <br>
Risk: The security summary marks the release suspicious because automatic repair behavior has limited user controls. <br>
Mitigation: Install only when unattended OpenClaw recovery is intended, and consider disabling lifecycle scripts or auto-fix behavior until the operator accepts the actions. <br>


## Reference(s): <br>
- [Auto-Heal on ClawHub](https://clawhub.ai/zacharyzax/auto-heal) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and JavaScript code behavior] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill behavior centers on OpenClaw CLI commands, local configuration updates, log output, and state JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
