## Description: <br>
Provides on-demand rollback protection for OpenClaw configuration changes by restoring the latest backup and restarting Gateway when Gateway is unhealthy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[segasonicye](https://clawhub.ai/user/segasonicye) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to add a manual safety check around OpenClaw configuration edits. It can restore the most recent backup of openclaw.json and restart Gateway when the local Gateway does not report an active state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog can replace the active OpenClaw configuration with the latest backup and force-restart Gateway. <br>
Mitigation: Review before installing or running, keep current backups, and run only when intentional rollback behavior is acceptable. <br>
Risk: If configured for background monitoring, unclear trigger boundaries could cause an unexpected rollback when Gateway appears unhealthy. <br>
Mitigation: Keep usage manual unless background monitoring is explicitly configured and audited. <br>


## Reference(s): <br>
- [Config Guard on ClawHub](https://clawhub.ai/segasonicye/config-guard) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Artifact skill.json](artifact/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown usage guidance with bash command examples and a shell watchdog script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May copy files under ~/.openclaw, write /tmp/openclaw-watchdog.log, and force-restart the local OpenClaw Gateway.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
