## Description:

Claw Operations Manager provides a multilingual OpenClaw operations dashboard for audit logging, permission checks, file monitoring, git-based snapshots, and rollback guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a3273283](https://clawhub.ai/user/a3273283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to monitor OpenClaw activity, review local operation history, manage permissions, and prepare recovery actions through snapshots and rollback workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes powerful local audit, snapshot, and rollback operations with weak controls.

Mitigation: Run it only on a trusted machine, avoid privileged accounts, and review operations before allowing rollback actions.

Risk: The dashboard can expose operational controls if port 8080 is reachable from a network.

Mitigation: Use the dashboard locally and do not expose port 8080 to a network.

Risk: Snapshots may include sensitive directories such as ~/.ssh or broad home-directory paths.

Mitigation: Remove ~/.ssh and whole-home snapshot paths from defaults, limit snapshot scope, and protect audit and snapshot storage.

Risk: Rollback is experimental and should not be treated as a backup system.

Mitigation: Use dry runs where available and keep an independent backup before relying on restore actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a3273283/skills/claw-ops-manager)
- [API reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe local dashboard, audit, snapshot, and rollback workflows; users should review commands before execution.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
