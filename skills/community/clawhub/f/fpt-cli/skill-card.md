## Description: <br>
This skill helps agents install, configure, inspect, and operate fpt-cli for Autodesk Flow Production Tracking and ShotGrid workflows, especially authentication setup, schema and entity reads, structured searches, and safe write previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loonghao](https://clawhub.ai/user/loonghao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical operators use this skill to guide agents through fpt-cli installation, authentication, command inspection, schema/entity queries, structured search patterns, and dry-run-first mutation workflows for Flow Production Tracking or ShotGrid sites. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use credentials for a ShotGrid/FPT site. <br>
Mitigation: Use scoped or short-lived credentials where possible, inject secrets through environment variables, and avoid exposing real secrets in chat or logs. <br>
Risk: Entity writes or deletes could affect production tracking data if executed without review. <br>
Mitigation: Review dry-run output before real writes and require explicit confirmation for destructive operations. <br>
Risk: Large or poorly scoped API responses can consume excessive agent context. <br>
Mitigation: Request only needed fields, use narrow commands, and inspect command/schema contracts at runtime before composing queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loonghao/fpt-cli) <br>
- [Install and authentication reference](references/install-and-auth.md) <br>
- [Query patterns reference](references/query-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers JSON CLI output, runtime schema introspection, scoped fields, dry-run previews before writes, and environment-based credential handling.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
