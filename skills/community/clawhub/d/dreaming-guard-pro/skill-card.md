## Description:

Dreaming Guard Pro helps agents monitor OpenClaw dreaming context growth, archive and compress accumulated files, protect process memory, and produce recovery-oriented health reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuangzhanzhiwang](https://clawhub.ai/user/kuangzhanzhiwang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor and manage OpenClaw dreaming context files so growth, memory pressure, archive and compression actions, and crash recovery can be reviewed or automated.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent monitoring and automation can affect local OpenClaw files and process state if enabled without review.

Mitigation: Install under an unprivileged account, review configuration and cron usage before enabling daemon or scheduled execution, and keep automatic actions scoped to intended OpenClaw paths.

Risk: Restore, cleanup, compression, or recovery behavior may overwrite or remove useful context if archives or paths are untrusted or misconfigured.

Mitigation: Use trusted archive locations, maintain backups, and run with dry-run or manual review before enabling automatic compression, cleanup, or recovery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kuangzhanzhiwang/skills/dreaming-guard-pro)
- [README.md](README.md)
- [ARCHITECTURE.md](ARCHITECTURE.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, plain text, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Health reports and actions may reflect local filesystem, archive, configuration, and process-memory state.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
