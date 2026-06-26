## Description: <br>
Call Claude Code as a non-interactive coding agent on a remote machine through OpenClaw Node. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xxuzzwz](https://clawhub.ai/user/xxuzzwz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate coding tasks to Claude Code running on a remote OpenClaw Node, especially when coordinating remote projects, worktrees, non-interactive shells, or multi-agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote Claude Code execution can run high-privilege shell, git, file, or network actions on the node. <br>
Mitigation: Prefer read-only or tightly scoped permission modes, review commands before execution, and use permission-bypass modes only on trusted nodes and repositories. <br>
Risk: API credentials used by non-interactive shells can be exposed through weak shell-profile handling or troubleshooting output. <br>
Mitigation: Store API keys with strict access controls, load them only where needed, and avoid printing any part of secrets while diagnosing remote execution. <br>


## Reference(s): <br>
- [Permission Mode Details](references/permissions.md) <br>
- [Remote-Specific Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with shell command and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command templates for Claude Code permission modes, remote execution, worktree setup, and environment loading.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
