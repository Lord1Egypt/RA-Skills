## Description: <br>
Agent Swarm orchestrates specialized agents to break down complex work, run subtasks in parallel or sequence, and integrate the results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lixiang1076](https://clawhub.ai/user/lixiang1076) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multiple specialized agents for complex projects that need planning, research, coding, writing, design, analysis, review, or automation. It is intended for workflows where task decomposition, parallel execution, role-specific handoffs, and final result synthesis improve speed or quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Some agent roles can execute commands, automate a browser, create scheduled jobs, and make broad file changes. <br>
Mitigation: Review the OpenClaw agent configuration before use, disable exec, process, browser, and cron permissions for roles that do not need them, and require exact command and schedule previews before execution. <br>
Risk: Persistent experience memory can accidentally retain sensitive information. <br>
Mitigation: Keep credentials and private data out of memory entries, periodically review stored experience files, and remove entries that contain sensitive or unnecessary details. <br>
Risk: Helper scripts accept agent identifiers and base paths that affect local files. <br>
Mitigation: Use trusted agent IDs and base paths, review generated directories and configuration changes, and avoid running the scripts against untrusted paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lixiang1076/agent-swarm-ex) <br>
- [Multi-agent setup guide](references/setup-guide.md) <br>
- [CHJ-Private model configuration guide](references/chj-private-guide.md) <br>
- [CHJ-Private configuration template](references/chj-private-config-template.json) <br>
- [Task statistics and cost analysis template](references/statistics-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, and JSON configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill expects a final execution summary with agent-level timing, token, status, and cost information after coordinated work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
