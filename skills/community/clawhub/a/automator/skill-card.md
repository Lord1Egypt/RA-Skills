## Description:

Automate macOS tasks by composing and executing Automator workflows through automator CLI and AppleScript control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and macOS power users use this skill to run, compose, inspect, and troubleshoot Automator workflows with explicit confirmation for writes and destructive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automator workflows can modify, overwrite, delete, or batch-change local files or application data.

Mitigation: Require the user to confirm the workflow path, target, side effects, and rollback plan, with two explicit confirmations before destructive execution.

Risk: Ambiguous workflow paths, unbounded stdin, or mismatched Automator action names can cause failed runs or unintended automation behavior.

Mitigation: Use absolute workflow paths, bounded inputs, preflight checks for automator and osascript, and read back workflow state after changes.

Risk: Local run diagnostics and workflow paths may reveal information about the user's macOS environment.

Mitigation: Keep workflow paths, action names, and diagnostics local by default and avoid sending workflow content to external services.

## Reference(s):

- [macOS Automator ClawHub skill page](https://clawhub.ai/ivangdavila/skills/automator)
- [Skill homepage](https://clawic.com/skills/automator)
- [Interface Matrix](interface-matrix.md)
- [Execution Guardrails](execution-guardrails.md)
- [Workflow Authoring With AppleScript](workflow-authoring.md)
- [Troubleshooting](troubleshooting.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local macOS Automator workflow guidance; requires macOS with automator and osascript available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
