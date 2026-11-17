## Description:

This skill helps developers and database engineers collect Redis migration inputs, generate RedisShake configuration, and deploy, start, stop, monitor, or troubleshoot RedisShake jobs locally or over SSH.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DBAs, and migration engineers use this skill to plan and operate RedisShake migrations from user-supplied Redis, SSH, and deployment details. It is intended for Redis and RedisShake workflows on Linux servers where the user provides the target hosts, credentials, and operating mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide SSH, Redis credential use, remote command execution, sudo/systemd operations, and process management.

Mitigation: Use only scoped credentials, confirm every host and command before execution, prefer non-root operation, and avoid systemd or sudo unless production persistence requires it.

Risk: Generated shake.toml files can contain cleartext Redis passwords.

Mitigation: Review the generated configuration, keep file permissions restricted with chmod 600, avoid committing or sharing the file, and use the documented envsubst approach for stronger credential handling.

Risk: Target-emptying or Redis flush behavior can cause irreversible data loss.

Mitigation: Require explicit review of destructive options, use the documented double confirmation for empty_db_before_sync, and block FLUSHALL or FLUSHDB in generated filters unless deliberately approved.

Risk: Migration success and data consistency are not automatically guaranteed by the skill.

Mitigation: Have a DBA review production plans and verify completion with logs, dbsize comparisons, redis-cli sampling, or redis-full-check as appropriate.

Risk: Batch operations can affect multiple servers if an incorrect host list is used.

Mitigation: Avoid batch execution until the complete host list and intended operation have been reviewed and confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-migration-dbm-redis-shake-migration)
- [Reader Mode Details](references/reader-modes.md)
- [SSH Remote Execution Details](references/remote-ssh.md)
- [Config Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TOML and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include masked credential displays, confirmation prompts, RedisShake configuration snippets, SSH commands, status summaries, and troubleshooting guidance.]

## Skill Version(s):

0.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
