## Description: <br>
Event Manager helps agents create, edit, query, and export novel event records with causality chains, timelines, and multi-thread narrative tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and writing agents use this skill during novel planning to manage event files, inspect causal relationships, and export a chapter timeline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local CLI can create, update, export, and delete event files in the selected project directory. <br>
Mitigation: Review the project path before running commands, keep backups for important event files, and confirm delete operations intentionally. <br>
Risk: Dependency ranges use lower bounds, which can reduce reproducibility across environments. <br>
Mitigation: Pin dependency versions for controlled or repeatable deployments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuzhihui886/event-manager) <br>
- [API Reference](references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [YAML event files, Markdown timeline exports, and CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local filesystem operations create, update, delete, query, and export event records in a chosen project directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
