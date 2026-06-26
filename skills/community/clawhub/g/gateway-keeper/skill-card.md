## Description: <br>
Gateway Keeper installs an OS-level watchdog that checks OpenClaw gateway health, restarts the gateway when it appears down, and records a recovery signal for interrupted sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[russellfei](https://clawhub.ai/user/russellfei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators responsible for OpenClaw deployments use this skill to add recurring gateway health checks, automatic restarts, and recovery prompts after a crash. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs recurring background automation that monitors and restarts the OpenClaw gateway. <br>
Mitigation: Install it only when continuous gateway monitoring is intended, and review the scheduled cron or task entry before use. <br>
Risk: Recovery behavior can influence future agent work after a gateway restart. <br>
Mitigation: Review the HEARTBEAT.md recovery block and require fresh approval before retrying file, deployment, account, or external-service changes. <br>
Risk: The documentation includes Windows administrator PowerShell commands, but the provided artifact evidence does not include the referenced PowerShell scripts. <br>
Mitigation: Do not run the Windows commands unless the missing scripts are provided and reviewed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and PowerShell command examples plus JSON recovery-file examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install, uninstall, gateway check, and recovery workflow guidance for OpenClaw environments.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
