## Description: <br>
Use this skill only when the user explicitly asks for a dry-run cleanup inventory, disk-space cleanup, deletion review, or recoverable archiving of generated workspace artifacts in a coding repo, such as caches, logs, test reports, screenshots, temporary databases, eval outputs, build outputs, or agent scratch files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hollis9087](https://clawhub.ai/user/hollis9087) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to inventory, review, archive, or remove generated workspace artifacts while preserving source changes, secrets, datasets, and other review-required files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace cleanup can affect high-value local files or privileged workflow outputs if commands are approved without review. <br>
Mitigation: Use the skill's dry-run inventory first, review exact paths and actions before cleanup, keep activity inside the resolved workspace root, and prefer recoverable archives unless permanent deletion is explicitly requested. <br>
Risk: Sensitive credentials, private keys, token files, local databases, datasets, and tracked source changes may be present in the workspace. <br>
Mitigation: Follow the security guidance and skill rules that classify secret-looking paths and tracked changes as protected, and treat databases, datasets, archives, and unclear files as review-required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hollis9087/agent-workspace-hygiene) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with concise reports, inline shell commands, and optional JSON inventory summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to dry-run inventory, asks for confirmation before file changes, and prefers recoverable archives over permanent deletion.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
