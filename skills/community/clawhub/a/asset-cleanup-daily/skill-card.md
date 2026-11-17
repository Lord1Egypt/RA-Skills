## Description:

Runs a scheduled cleanup that removes expired temporary files, old JSONL logs, stale lock and backup files, and expired asset records, then writes a JSON audit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to run daily infrastructure maintenance for a JUEJIN_HOME workspace, reclaim disk space, and record the cleanup outcome. It is intended for scheduled asset and file cleanup, not real-time asset health monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform irreversible local, database, and remote asset deletion.

Mitigation: Run with --dry-run first, verify the reported deletion scope, and enable the daily cron job only in a controlled JUEJIN_HOME environment.

Risk: Cleanup behavior depends on trusted expiry data, credentials, and the delegated asset cleanup script.

Mitigation: Use only trusted tenant_assets expiry data, AList credentials, and delegated scripts/asset_cleanup.py before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/asset-cleanup-daily)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON report with human-readable operational guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports a dry-run mode; writes an audit report under data/audit when the workspace data directory is available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
