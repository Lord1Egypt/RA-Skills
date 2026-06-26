## Description: <br>
Provides the `oce` command, a validation-aware, transaction-capable editing toolkit for agents working with source code across common programming and markup languages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to read, search, edit, validate, format, and recover changes in source-code workspaces. It is intended for bug fixes, feature work, refactors, code review, configuration changes, and coordinated multi-file edits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad local file-changing authority. <br>
Mitigation: Use it only in workspaces where the agent is allowed to edit files, review diffs before accepting changes, and run the project's tests for important edits. <br>
Risk: Persistent installation and bundled dependency behavior may be more permissive than a single-session workflow needs. <br>
Mitigation: Prefer direct invocation or a session-only alias unless persistent installation is required, and review the install script and dependencies first. <br>
Risk: Formatting and validation commands may execute local project tooling or behave unexpectedly on untrusted repositories or unusual file paths. <br>
Mitigation: Avoid running those commands on untrusted repositories, keep paths simple and reviewed, and use transactions for coordinated multi-file edits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/encryptshawn/agentic-cli-coding) <br>
- [README](artifact/README.md) <br>
- [JSON Output Schema](artifact/references/json-schema.md) <br>
- [Workflows](artifact/references/workflows.md) <br>
- [Language Support Matrix](artifact/references/language-support.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command guidance, with optional JSON command output from `oce`] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can create backups, transactions, diffs, validation results, and edited files in the target workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
