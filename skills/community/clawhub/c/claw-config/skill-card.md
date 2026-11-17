## Description:

Claw Config helps OpenClaw agents identify their own configuration slice, inspect schema and documentation, diagnose setup issues, and plan or apply guarded configuration changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhili1004](https://clawhub.ai/user/zhili1004)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an OpenClaw agent inspect its own identity, schema, documentation, diagnostics, and configuration patch plan before making agent-scoped changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and modify persistent OpenClaw configuration.

Mitigation: Require human review of the dry-run plan before using apply, and rely on the skill's backup and rollback behavior for failed writes.

Risk: Documentation fetching and cache behavior may expose users to under-scoped URL or stale-documentation issues.

Mitigation: Use known OpenClaw documentation slugs, avoid full URLs, and refresh documentation only from trusted interactive contexts.

Risk: Shared-section or array-replacement changes can affect more configuration than the caller intended.

Mitigation: Avoid --force-shared unless an operator explicitly approves it, and inspect dry-run diffs for whole-array or shared-section replacement before applying.

## Reference(s):

- [Claw Config skill page](https://clawhub.ai/zhili1004/skills/claw-config)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [Artifact README](README.md)
- [Examples README](examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, shell commands]

**Output Format:** [Plain text or JSON command output, Markdown reports, and JSON5 configuration patch files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only and diagnostic commands are cron-safe; apply performs configuration writes and is blocked in cron context.]

## Skill Version(s):

0.1.0 (source: server release metadata, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
