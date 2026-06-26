## Description: <br>
Advanced multi-agent development system for complex software projects that uses Orchestrator, Builder, and Reviewer agents to decompose modules, implement code, and perform iterative quality reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subaru0573](https://clawhub.ai/user/subaru0573) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate complex software builds across orchestrator, builder, and reviewer agents, with module decomposition, progress tracking, implementation, review, and end-to-end smoke testing. It is intended for larger multi-module work rather than simple edits, code reading, or single-file changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant broad local file, command execution, agent-spawning, dashboard, and logging authority. <br>
Mitigation: Install and run it only in a dedicated project workspace, container, or VM; use trusted Builder and Reviewer agents; and restrict session visibility and agent allowlists. <br>
Risk: The dashboard serves project files and logs from the local workspace, which can expose secrets if the workspace contains credentials or sensitive files. <br>
Mitigation: Keep the dashboard bound to localhost, use a workspace without secrets, and review which files and logs are exposed before running the dashboard. <br>
Risk: Dashboard Markdown sanitization and log-retention behavior may need hardening before broader use. <br>
Mitigation: Review and improve dashboard sanitization and log-retention controls before using the skill with sensitive or untrusted projects. <br>


## Reference(s): <br>
- [Deep Coding Harness Architecture](references/architecture.md) <br>
- [Orchestrator Rules](references/orchestrator-rules.md) <br>
- [ClawHub skill page](https://clawhub.ai/subaru0573/deep-coding-p) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, configuration snippets, project files, logs, and dashboard output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces project request files, project-state JSON, per-agent logs, generated code, review records, and localhost dashboard data when used with the bundled assets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
