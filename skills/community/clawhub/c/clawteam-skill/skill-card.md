## Description: <br>
Multi-agent swarm coordination via the ClawTeam CLI for creating agent teams, running agents in parallel, coordinating dependent tasks, broadcasting messages, monitoring kanban progress, and launching pre-built team templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xybio](https://clawhub.ai/user/xybio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-agent work through the external `clawteam` CLI, including team creation, task dependency management, worker spawning, progress monitoring, and cleanup checkpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can spawn local agents and modify git worktrees through the external `clawteam` CLI. <br>
Mitigation: Install and pin the CLI from a trusted source, start in a disposable repository, keep approval prompts enabled, and monitor spawned agents. <br>
Risk: Subprocess or custom backend modes can run delegated commands in the local environment. <br>
Mitigation: Use subprocess and custom backend modes only in trusted repositories and environments, and require explicit operator approval before high-impact actions. <br>
Risk: Team state, messages, plans, costs, and worktree metadata can persist under local ClawTeam state directories. <br>
Mitigation: Clean up ClawTeam state and worktrees after use, and avoid placing secrets in tasks, chat messages, or worktrees. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xybio/clawteam-skill) <br>
- [ClawTeam OpenClaw project](https://github.com/win4r/ClawTeam-OpenClaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external `clawteam` binary to be installed and available on PATH.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
