## Description: <br>
Task Management is a local task-management skill for creating, finding, updating, deleting, and summarizing tasks from an agent workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xfwgithub](https://clawhub.ai/user/xfwgithub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to manage project tasks through agent or CLI commands and an optional local web UI. It supports task lifecycle tracking, review handoffs, task statistics, and cleanup of stale in-progress work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional web UI can expose or modify local task data without authentication if reachable from a shared network. <br>
Mitigation: Bind the web UI to localhost or protect it with a firewall; add authentication before exposing it beyond the local machine. <br>
Risk: State-changing commands can create, update, approve, cancel, or delete task records. <br>
Mitigation: Review command intent before execution and require explicit human approval for completion or destructive deletion workflows. <br>
Risk: Latest-download installation paths may pull unpinned artifacts. <br>
Mitigation: Prefer pinned releases or verified source packages for installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xfwgithub/ai-task-management) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [Agent Configuration](artifact/claude.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses from task commands, with Markdown and shell-command guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores task state in a local SQLite database when used with the packaged command or web UI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
