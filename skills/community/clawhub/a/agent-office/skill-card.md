## Description: <br>
Agent Office creates and manages local AI employees as independent HTTP workers for multi-agent office automation, supporting OpenClaw, Hermes, DeerFlow, CLI, external, and stub engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jast-hub](https://clawhub.ai/user/jast-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to create, configure, run, inspect, and remove local AI worker teams for office automation, software delivery, publishing workflows, and delegated task execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local workers can run commands and write files on the host. <br>
Mitigation: Install only when a local multi-agent worker system is intended; keep workers bound to localhost and avoid broad workspace paths or untrusted custom CLI commands. <br>
Risk: DeerFlow mode can install or update remote runtime code and execute tasks with host file access. <br>
Mitigation: Use trusted DeerFlow repositories only, avoid untrusted extra mounts, and treat DeerFlow workers as capable of host command execution and file writes. <br>
Risk: Memory and external upstream integrations can persist or forward task content and summaries. <br>
Mitigation: Configure MEMORY_CLI or external upstream URLs only when the operator accepts that task data may be stored or sent to those services. <br>


## Reference(s): <br>
- [Agent Office on ClawHub](https://clawhub.ai/jast-hub/agent-office) <br>
- [ClawHub homepage](https://clawhub.com) <br>
- [DeerFlow runtime repository](https://github.com/bytedance/deer-flow.git) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands, JSON configuration examples, and local worker management guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local worker directories, state files, logs, runtime files, and worker configuration when the documented commands are executed.] <br>

## Skill Version(s): <br>
1.5.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
