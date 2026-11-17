## Description:

CPA Manager helps CLIProxyAPI operators scan authentication-file inventory, detect 401 and quota states, maintain account pools, upload auth files, refill pools, and track local status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[violin321](https://clawhub.ai/user/violin321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage CLIProxyAPI authentication-file pools, including health scans, 401 and quota review, controlled cleanup, upload, refill, and local audit tracking. It is intended for CPA deployments with a management API and local auth-file directory access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact account maintenance can delete, disable, re-enable, upload, or refill CPA auth files.

Mitigation: Run scan first, review exported 401 and quota results, keep backups outside the CPA auth tree, and restrict maintain, maintain-refill, upload, and --yes to authorized operators.

Risk: Management tokens, auth files, SQLite state, logs, and JSON exports may contain sensitive operational data.

Mitigation: Use HTTPS or loopback-only management endpoints, narrowly scoped tokens, private working directories, placeholder-only shared configs, and do not commit runtime config or generated outputs.

Risk: Preview controls may not fully model all state changes, and --no-delete-401 is not a full dry run.

Mitigation: Treat preview results as advisory, prefer the scan-review-delete-rescan workflow for one-off cleanup, and verify CPA inventory after each maintenance action.

Risk: auto_register and register_command can execute local commands during refill workflows.

Mitigation: Keep auto_register disabled unless the command, working directory, timeout, environment, and outputs have been reviewed for the deployment.

Risk: High worker counts can overload the CPA service or produce unreliable probe outcomes.

Mitigation: Start with low probe and action worker counts, monitor service health and logs, and increase concurrency gradually only when the environment can support it.

## Reference(s):

- [ClawHub CPA Manager Release](https://clawhub.ai/violin321/skills/cpa-manager)
- [Publisher Profile](https://clawhub.ai/user/violin321)
- [CPA Warden Upstream Project](https://github.com/fantasticjoe/cpa-warden)
- [CPA Warden Manual Workflow](references/workflow.md)
- [Safety Guidelines](safety.md)
- [Troubleshooting Guide](troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and JSON or SQLite-backed operational outputs from bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance and script-driven local files such as logs, SQLite state, and JSON scan exports when the user runs the CPA tools.]

## Skill Version(s):

1.1.0 (source: server release and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
