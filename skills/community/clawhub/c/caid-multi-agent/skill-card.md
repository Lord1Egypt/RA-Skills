## Description: <br>
Coordinate multiple sub-agents to collaboratively complete long-horizon software engineering tasks using the CAID (Centralized Asynchronous Isolated Delegation) paradigm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncatbot](https://clawhub.ai/user/simoncatbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan, delegate, verify, and integrate long-horizon software engineering work across multiple isolated sub-agents. It is most relevant when a task has clear dependencies, parallelizable implementation units, and executable tests for integration review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow includes destructive git cleanup and reset examples that can remove local work if run in the wrong directory. <br>
Mitigation: Confirm the current path and worktree target with git status before cleanup, and require explicit review before running git reset --hard or rm -rf. <br>
Risk: The skill instructs agents to create and merge branches, install dependencies, run tests, push changes, and spawn sub-agents. <br>
Mitigation: Use it only in repositories where those actions are authorized, and constrain spawned agents to assigned worktrees and target files. <br>


## Reference(s): <br>
- [CAID Multi-Agent Examples](references/examples.md) <br>
- [async-swe-agents GitHub repository](https://github.com/JiayiGeng/async-swe-agents) <br>
- [ClawHub skill page](https://clawhub.ai/simoncatbot/caid-multi-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON task assignments and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Coordinates branch-and-merge workflows, isolated git worktrees, sub-agent task delegation, verification commands, and final integration review.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
