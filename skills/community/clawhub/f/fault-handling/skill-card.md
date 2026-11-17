## Description:

When an operations user needs fault handling, remote script execution, service restart, or disk cleanup, this skill runs a script through the run-script API and polls execution-history for the result.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lerwee](https://clawhub.ai/user/lerwee)

### License/Terms of Use:

MIT-0

## Use Case:

Operations engineers use this skill to run preset or user-supplied maintenance scripts on specified remote hosts, then receive a structured execution report with per-host status and logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute remote scripts, restart services, and clean disk space on managed hosts, which may disrupt systems if the target host or script is wrong.

Mitigation: Install only where this operational API is intended to make managed-host changes, and require users to review the exact target hosts and script or preset before each run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lerwee/skills/fault-handling)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON execution reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include execution ID, task name, status, elapsed time, per-step output, and per-host stdout/status when available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
