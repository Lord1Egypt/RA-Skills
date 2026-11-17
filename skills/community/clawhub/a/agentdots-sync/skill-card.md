## Description:

Use when users ask to sync, restore, apply, back up, push, or roll back local agent instructions, rules, or skills for Codex, Claude Code, OpenCode, Grok Build, CodeBuddy Code, WorkBuddy, or another Agent Skills-compatible platform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ferbylv](https://clawhub.ai/user/ferbylv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, plan, sync, restore, back up, push, and roll back selected local agent configuration assets against a Git remote. It is intended for filesystem-capable agent environments where Python and Git are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved sync, restore, apply, push, or rollback operations can persist changes to local agent configuration assets across future sessions.

Mitigation: Review the resolved platform, root, selected assets, backup directory, remote, and branch before approving any command that uses --yes.

Risk: Using the wrong platform profile, root, asset list, remote, or branch can copy or push unintended agent instructions.

Mitigation: Run read-only inspection commands first, require explicit values when defaults are uncertain, and stop on validation, Git, lock, or permission failures.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and plain-text CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Plans identify the selected platform, action, local root, assets, backup directory, remote, and branch before any approved mutation.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
