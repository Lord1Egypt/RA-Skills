## Description: <br>
A production-grade AI coding agent that enforces JT directives by verifying code, running parallel sub-agents, logging mistakes, and preserving edit integrity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iyang1016](https://clawhub.ai/user/iyang1016) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this agent skill to guide coding work with mandatory verification, edit-safety checks, parallel sub-agent workflows, and persistent mistake or memory logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may make broad autonomous repository changes, including modifications or deletions. <br>
Mitigation: Require explicit approval for destructive actions and broad refactors, then review diffs and verification results before accepting changes. <br>
Risk: Persistent memory and gotchas logging may capture sensitive user, project, or repository details. <br>
Mitigation: Disable or closely review memory logging on sensitive repositories and inspect generated memory files before committing or sharing the workspace. <br>
Risk: Parallel sub-agent workflows can increase the scope and complexity of changes. <br>
Mitigation: Use restricted permission modes for high-risk work and require a human review checkpoint before merging multi-agent outputs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iyang1016/clawder-publish) <br>
- [Clawder agent definition](artifact/clawder/agent.md) <br>
- [Clawder agent card metadata](artifact/clawder/agent-card.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code, shell command, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify repository files and write memory files when used by an agent with filesystem permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, package.json, agent-card.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
