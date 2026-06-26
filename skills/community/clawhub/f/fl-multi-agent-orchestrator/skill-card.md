## Description: <br>
Production-grade multi-agent orchestration patterns for decomposing complex tasks into parallel subtasks, coordinating agent swarms, building sequential pipelines, and running review cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PhilipStark](https://clawhub.ai/user/PhilipStark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical teams use this skill to plan and coordinate multi-agent work across research, coding, review, testing, documentation, and infrastructure workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Coordinated agents can make broad code changes or invoke commands if given those tools. <br>
Mitigation: Review the execution plan first, run on a branch or sandbox, limit each agent's file scope and tools, and require approval before Bash, deployment, rollback, or broad file changes. <br>
Risk: Parallel agents can conflict when touching the same files or shared resources. <br>
Mitigation: Use the skill's file-scope restrictions, dependency planning, and file locking guidance before allowing multiple agents to edit the same workspace. <br>
Risk: Agents may access secrets or credentials if the workspace and tools are not scoped. <br>
Mitigation: Block secrets and credential files before running agent workflows and use minimal tool permissions for each role. <br>
Risk: Budget, timeout, or retry settings can allow runaway work if left unbounded. <br>
Mitigation: Set per-agent and total budgets, max turns, timeouts, and retry limits before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/PhilipStark/fl-multi-agent-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/PhilipStark) <br>
- [claude-swarm source material](https://github.com/affaan-m/claude-swarm) <br>
- [claude_code_agent_farm source material](https://github.com/mckaywrigley/claude_code_agent_farm) <br>
- [TubeFlow source material](https://github.com/webnestify/tubeflow) <br>
- [Author profile referenced by package README](https://threads.net/@felipe_bmottaa) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and YAML configuration examples, shell command snippets, prompts, and structured orchestration reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include execution plans, role prompts, dependency graphs, budget guidance, review criteria, and partial-success reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
