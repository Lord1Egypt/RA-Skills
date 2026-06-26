## Description: <br>
Agent Swarm Dev Team helps orchestrate multiple AI coding agents, including Codex and Claude Code, to work on development tasks across isolated worktrees and tmux sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyhot](https://clawhub.ai/user/sunnyhot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate AI coding agents for implementation, review, monitoring, and follow-up work across branches, worktrees, and pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks this skill suspicious because it defaults to elevated, approval-bypassing agent execution. <br>
Mitigation: Remove or override the dangerous default agent arguments before use and require explicit per-task approval for privileged actions. <br>
Risk: The release references runtime scripts for launching and checking agents that are not included in the artifact. <br>
Mitigation: Inspect, provide, and review the missing run-agent.sh and check-agents.sh scripts before relying on the workflow. <br>
Risk: The initialization script uses a hardcoded local install path and writes local files and permissions. <br>
Mitigation: Change the install path for the target environment and run the setup only in a reviewed, disposable workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sunnyhot/agent-swarm-dev-team) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and Node.js initialization code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup guidance for tmux, git worktrees, agent review workflows, and monitoring scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and package.json also specify 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
