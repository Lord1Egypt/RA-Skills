## Description:

Config Modification helps agents guard OpenClaw JSON configuration changes with syntax validation, risk checks, rollback verification, Gateway health checks, and optional local file watching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to validate and recover local OpenClaw configuration changes before or after edits to sensitive JSON config files. It is intended for workflows that need safer edits, snapshots, rollback checks, health checks, and command guidance around OpenClaw Gateway configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent local watcher can automatically modify OpenClaw configuration and restart the Gateway.

Mitigation: Install only where that automation is acceptable, scope watched paths explicitly to ~/.openclaw, and keep watcher startup under operator control.

Risk: Diffs and logs may expose token, password, API-key, or credential fields from configuration files.

Mitigation: Redact sensitive fields before displaying or storing diff output and review generated logs before sharing them.

Risk: Rollback can restore the wrong file or fail to recover safely if snapshots are not bound to the exact validated config file.

Mitigation: Bind snapshots and rollback targets to the same validated path and verify rollback availability before applying risky changes.

Risk: Validation infrastructure failures can allow a change to proceed when checks were not actually completed.

Mitigation: Treat validation or watcher failures as fail-closed conditions requiring manual review before continuing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/config-modification)
- [fswatch integration design](artifact/references/fswatch-integration.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands, Python snippets, validation summaries, and log paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workflow guidance and command output for OpenClaw configuration validation, rollback, and file-watch operation; no network service output is described by the skill.]

## Skill Version(s):

2.6.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
