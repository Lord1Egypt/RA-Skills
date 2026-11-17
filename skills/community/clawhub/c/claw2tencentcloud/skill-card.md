## Description:

This skill helps users migrate OpenClaw data to Tencent Cloud instances through single-instance migration, batch migration to Tencent Cloud Lighthouse or CVM instances, or custom migration planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoikin-yiu](https://clawhub.ai/user/hoikin-yiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to plan and execute OpenClaw data migrations between servers and Tencent Cloud instances, including single-instance, batch, and custom migration scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration commands can stop the source OpenClaw instance and overwrite existing destination data.

Mitigation: Require explicit user confirmation, create backups before migration, and prepare a rollback plan before running overwrite or restart commands.

Risk: The skill asks for SSH and cloud API credentials with broad operational impact.

Mitigation: Use short-lived, least-privilege credentials and protect secrets from logs, transcripts, shell history, and shared files.

Risk: The documented SSH commands disable strict host key checking and support password-based login.

Mitigation: Prefer SSH key authentication with verified host keys before connecting to source or destination hosts.

Risk: The batch workflow downloads and runs an external migration script.

Mitigation: Use a bundled or checksum-verified copy of the script and review it before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hoikin-yiu/skills/claw2tencentcloud)
- [Migration Commands Reference](references/migration_commands.md)
- [Batch Migration Script](https://go2tencentcloud-1251783334.cos.ap-guangzhou.myqcloud.com/others/claw2tencentcloud.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands, migration steps, and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask the user for source host details, login credentials, cloud API credentials, instance pair mappings, region information, and migration constraints.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
