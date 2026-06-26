## Description: <br>
Persistent task queue system with INTAKE and DISPATCHER modes for queuing natural-language tasks, dispatching subagents, and reporting task completions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to keep a persistent queue of tasks, dispatch work asynchronously, and receive status or completion messages as tasks finish or become blocked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can establish long-running task execution by adding heartbeat and recurring dispatcher behavior. <br>
Mitigation: Require explicit user confirmation before first-run setup and document how to pause or remove dispatcher entries. <br>
Risk: Broad natural-language triggers can queue or execute unintended tasks. <br>
Mitigation: Narrow trigger phrases, show parsed tasks before dispatch, and require confirmation for sensitive actions. <br>
Risk: Queued tasks may involve command execution, file writes, outbound messages, or subagent work with broad scope. <br>
Mitigation: Constrain tool permissions and workspace paths, require review for command execution and outbound messaging, and preserve blocked-task escalation for uncertain work. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chunhualiao/autonomous-task-runner) <br>
- [Queue Schema Reference](references/queue-schema.md) <br>
- [Task Types Catalog](references/task-types.md) <br>
- [Verification Guide](references/verification-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with task confirmations, status tables, JSON queue files, and shell or configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create persistent queue and archive files, task deliverables, HEARTBEAT.md entries, and recurring dispatcher configuration when enabled.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata, skill.yml, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
