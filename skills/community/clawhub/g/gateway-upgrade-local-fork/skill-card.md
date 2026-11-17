## Description:

Guides developers and operators through a local OpenClaw gateway upgrade workflow covering backup, upgrade, environment-variable merge, verification, rollback, and qmd/GPU health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to prepare and execute OpenClaw gateway upgrades on a local Linux host, preserve custom systemd service environment variables, validate qmd/GPU behavior, and recover with backups or rollback steps when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes high-impact local service, database, and package-management commands.

Mitigation: Review each command before execution, run it only on the intended OpenClaw host, and make verified backups before changing services, databases, packages, or binaries.

Risk: Generated reports and command output may include environment values or host-specific paths.

Mitigation: Redact environment values and sensitive paths before sharing reports, logs, or screenshots outside the local maintenance context.

Risk: Broad cleanup commands and shared temporary paths can affect unintended files or expose operational logs.

Mitigation: Replace broad cleanup targets and /tmp locations with private, reviewed paths, and inspect matched files before deleting or archiving them.

Risk: OpenClaw and qmd version drift can lead to ABI mismatch or degraded qmd behavior.

Mitigation: Pin OpenClaw and qmd versions where possible, check release notes before major upgrades, and rebuild native dependencies such as better-sqlite3 after qmd upgrades.

## Reference(s):

- [01 Pre-flight](references/01-preflight.md)
- [02 Backup](references/02-backup.md)
- [03 Upgrade](references/03-upgrade.md)
- [04 Post-flight](references/04-postflight.md)
- [05 Verify](references/05-verify.md)
- [06 Rollback](references/06-rollback.md)
- [80 Notes](references/80-notes.md)
- [qmd releases](https://github.com/tobi/qmd/releases)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command blocks, checklists, and report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local workflow guidance only; no credentials are required and the skill states that no data is forwarded.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
