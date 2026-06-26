## Description: <br>
agent-pack-n-go helps an OpenClaw agent migrate to a new Linux device by packaging configs, memory, skills, credentials, SSH keys, and selected system settings, then transferring and deploying them over SSH. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AICodeLion](https://clawhub.ai/user/AICodeLion) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers and OpenClaw operators use this skill to move, replicate, or recover a configured OpenClaw and Claude Code agent on another trusted Linux device. It is intended for device migration, team setup, lab-to-cloud moves, and point-in-time restoration workflows where the user wants the agent to guide SSH setup, packaging, transfer, deployment, and verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill clones credentials, tokens, SSH keys, and other sensitive agent state into a migration archive. <br>
Mitigation: Install only for an intentionally trusted target device; review archive contents before transfer, exclude or rotate unnecessary keys and tokens, and delete migration archives from both machines after verification. <br>
Risk: The workflow can make broad remote system and persistence changes, including cron jobs, /etc/hosts entries, proxy settings, OpenClaw services, and passwordless sudo setup. <br>
Mitigation: Inspect copied skills, memory, exec approvals, cron jobs, /etc/hosts, and proxy settings before use; remove passwordless sudo immediately after migration verification. <br>
Risk: Permission-skipping or automated remote execution can increase impact if the target host or transferred configuration is not fully trusted. <br>
Mitigation: Avoid permission-skipping execution unless the commands and generated files have been reviewed, and keep the old device available for rollback until the new deployment is verified. <br>


## Reference(s): <br>
- [OpenClaw Device Migration Operations Manual](references/migration-guide.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [OpenClaw Project](https://github.com/openclaw/openclaw) <br>
- [OpenClaw Migration Guide](https://docs.openclaw.ai/install/migrating) <br>
- [ClawHub skill page](https://clawhub.ai/AICodeLion/agent-pack-n-go) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated migration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces migration archives, setup/deploy scripts, progress files, and user-facing verification guidance during a device migration workflow.] <br>

## Skill Version(s): <br>
2.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
