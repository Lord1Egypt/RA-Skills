## Description:

Guides agents in using Claude Code as a managed coding agent for quick tasks and full worktree-to-PR automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiskyer](https://clawhub.ai/user/feiskyer)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to run Claude Code workflows for code analysis, implementation, review, task monitoring, and PR preparation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended workflows can perform high-impact repository actions such as edits, pushes, PR creation, and broad shell commands.

Mitigation: Run the skill only in an isolated, disposable workspace with least-privilege credentials and require human review before pushes, PRs, production access, or broad Bash execution.

Risk: Permission-bypass modes can allow automated changes without interactive approval.

Mitigation: Avoid --dangerously-skip-permissions unless containment is verified; prefer scoped allowed tools, read-only planning, or edit-only permission modes when possible.

Risk: Prompts, diffs, logs, or command output may contain sensitive project information.

Mitigation: Do not send sensitive diffs or logs to unapproved providers, and scrub credentials or confidential data before using external agent workflows.

## Reference(s):

- [Example Usage Scenarios](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/feiskyer/skills/claude-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured JSON or stream-json command output when the guided Claude Code workflow uses those modes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
