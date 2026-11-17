## Description:

A self-evolution engine for AI agents running on constrained hardware that analyzes runtime logs and dream cycles to propose, validate, and apply code improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to help an agent inspect its runtime logs, identify concrete failures, propose minimal fixes, validate them, and apply code changes with git-backed rollback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to read and modify workspace files, run git and python3, create commits, and keep an improvement log.

Mitigation: Run it only in a disposable or explicitly selected repository, review proposed changes before accepting them, and verify rollback behavior before using it on important code.

Risk: The security review flags the autonomous write and rollback workflow as broad without a clear user approval boundary.

Mitigation: Require explicit approval before file writes, command execution, and commits, and keep repository permissions scoped to the intended workspace.

Risk: The security guidance warns against use around private logs or credentials when network-backed review is involved.

Mitigation: Remove secrets from runtime logs, avoid private or credential-bearing workspaces, and use independent approval controls for any external review flow.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with FIND/REPLACE patches, code edits, shell commands, git commits, and JSON improvement logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits each improvement cycle to small code changes and records attempted, rejected, and applied improvements.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
