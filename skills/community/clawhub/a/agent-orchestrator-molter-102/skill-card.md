## Description: <br>
Multi-agent orchestration with 5 proven patterns - Work Crew, Supervisor, Pipeline, Council, and Auto-Routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[variable190](https://clawhub.ai/user/variable190) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multiple OpenClaw agents for parallel research, dynamic task decomposition, staged workflows, expert review, and automatic routing when a task benefits from multiple perspectives or structured delegation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tasks and intermediate outputs may be sent to multiple spawned sessions during orchestration. <br>
Mitigation: Keep tasks tightly scoped, avoid secrets or regulated data in prompts, and use least-privilege host permissions. <br>
Risk: Prompt injection and unsafe task propagation cannot be fully eliminated in multi-agent workflows. <br>
Mitigation: Keep the skill's safe-state mode enabled, rely on its sanitization and safety preamble behavior, and review generated outputs before code changes, deployments, publishing, or other high-impact actions. <br>
Risk: Multi-agent patterns can increase token cost and operational complexity. <br>
Mitigation: Limit agent counts and rounds, and use orchestration only for tasks where reliability, breadth, or speed justifies the overhead. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/variable190/agent-orchestrator-molter-102) <br>
- [Security notes](SECURITY.md) <br>
- [Examples guide](examples/README.md) <br>
- [Content pipeline example](examples/content-pipeline.json) <br>
- [Task router example](examples/task-router.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON summaries with command-line guidance and aggregated agent outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include synthesized consensus, routing decisions, staged workflow results, and recommendations that should be reviewed before high-impact use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
