## Description: <br>
Manage Cargo workspace users, API tokens, folders, roles, files, session records, and reports using the Cargo CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cargo-ai](https://clawhub.ai/user/cargo-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workspace administrators use this skill to manage Cargo workspace membership, roles, API tokens, folders, workspace files, and CLI issue reports. It can also guide agents through Cargo CLI session tracking when Claude Code hooks are intentionally enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace administration commands can invite or remove users, change roles, create tokens, and organize workspace resources. <br>
Mitigation: Run commands only with an account or token that has the intended workspace permissions, verify the active workspace with `cargo-ai whoami`, and review command arguments before execution. <br>
Risk: API token creation returns a token value once and can grant access matching the creating user's permissions. <br>
Mitigation: Store new token values immediately in a secrets manager, use descriptive token names, rotate unused tokens, and redact token values from reports and transcripts. <br>
Risk: Optional Claude Code session hooks can persist session records and transcript-derived summaries to Cargo. <br>
Mitigation: Enable the hooks only after reviewing the installer and confirming that persistent session tracking is acceptable for the workspace. <br>
Risk: The remote installer is documented as a shell pipeline. <br>
Mitigation: Inspect and verify the installer before running it instead of piping it directly into a shell. <br>


## Reference(s): <br>
- [Cargo Workspace Management on ClawHub](https://clawhub.ai/cargo-ai/cargo-workspace-management) <br>
- [Cargo Skills Homepage](https://github.com/getcargohq/cargo-skills) <br>
- [Response shapes](references/response-shapes.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [User management examples](references/examples/users.md) <br>
- [API token examples](references/examples/tokens.md) <br>
- [Folder examples](references/examples/folders.md) <br>
- [Report examples](references/examples/reports.md) <br>
- [Session tracking examples](references/examples/sessions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require the Cargo CLI, a Cargo account, and appropriate workspace permissions.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
