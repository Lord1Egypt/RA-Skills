## Description:

Provides on-demand 10-second automatic rollback protection when modifying openclaw.json to help restore OpenClaw Gateway stability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[segasonicye](https://clawhub.ai/user/segasonicye)

### License/Terms of Use:


## Use Case:

Developers and operators maintaining OpenClaw use this skill to watch Gateway health after configuration changes and restore the latest backup if the Gateway does not recover.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The watchdog may overwrite ~/.openclaw/openclaw.json and force-restart the OpenClaw Gateway.

Mitigation: Run it only with trusted backups, avoid elevated privileges, and require explicit approval or a dry-run path before enabling automatic recovery.

Risk: Recovery uses the latest timestamped backup without enough validation.

Mitigation: Validate backup contents, ownership, and permissions before restore, and keep known-good backups in a trusted private directory.

Risk: The watchdog log path is under /tmp, which may be unsuitable on shared systems.

Mitigation: Use a private log path with restrictive permissions and review logs for operational details before sharing.

## Reference(s):

- [Config Guard on ClawHub](https://clawhub.ai/segasonicye/skills/config-guard)
- [segasonicye Publisher Profile](https://clawhub.ai/user/segasonicye)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with a Bash script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May replace ~/.openclaw/openclaw.json, create failed-configuration backups, write a watchdog log, and force-restart the OpenClaw Gateway.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
