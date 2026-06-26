## Description: <br>
Runs coding tasks in a persistent tmux session with git worktree isolation and support for multiple interactive coding-agent CLIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanshenstarto](https://clawhub.ai/user/yuanshenstarto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to delegate build, fix, refactor, or review tasks to a selected coding agent while preserving a persistent tmux conversation and isolated git worktree. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spawned coding agents may see worktree files and linked environment secrets. <br>
Mitigation: Use task-scoped credentials, avoid symlinking real `.env` files when possible, and review what files are exposed before launch. <br>
Risk: The artifact includes a Claude Code launch mode that skips permission prompts. <br>
Mitigation: Avoid permission-skipping modes unless the operator explicitly accepts that risk for the run. <br>
Risk: Agent-generated commands and code changes may affect the project branch created for the task. <br>
Mitigation: Keep plan-first approval, inspect commands before forwarding approval, and test the preserved branch before merging. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/yuanshenstarto/claude-code-tmux) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [tmux](https://github.com/tmux/tmux) <br>
- [Claude Code](https://github.com/anthropics/claude-code) <br>
- [Codex](https://github.com/openai/codex) <br>
- [OpenCode](https://github.com/sst/opencode) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and relay instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational steps for spawning and supervising coding-agent sessions; no structured machine output is defined.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
