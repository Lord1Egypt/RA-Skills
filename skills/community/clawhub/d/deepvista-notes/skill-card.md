## Description: <br>
DeepVista Notes helps agents create, read, update, delete, and import user-managed DeepVista note cards through the DeepVista CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingconan](https://clawhub.ai/user/jingconan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to manage explicit notes in DeepVista, including listing, retrieving, creating, updating, deleting, quick-capturing, and importing note content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete notes in DeepVista. <br>
Mitigation: Require user confirmation before write or destructive commands. <br>
Risk: Imported files or URLs may store content the user did not intend to persist. <br>
Mitigation: Only import files or URLs the user explicitly wants stored in DeepVista. <br>
Risk: The skill depends on the deepvista-cli package and the deepvista-shared skill. <br>
Mitigation: Verify trust in the CLI package and required shared skill before installation. <br>


## Reference(s): <br>
- [DeepVista CLI homepage](https://cli.deepvista.ai) <br>
- [Deepvista Notes on ClawHub](https://clawhub.ai/jingconan/deepvista-notes) <br>
- [Publisher profile](https://clawhub.ai/user/jingconan) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance with inline DeepVista CLI commands and note URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write and destructive note operations require user confirmation; large imports should use content files to preserve exact content.] <br>

## Skill Version(s): <br>
0.1.0-alpha.21 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
