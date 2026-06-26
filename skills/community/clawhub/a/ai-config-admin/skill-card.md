## Description: <br>
Manage AI configuration for OpenClaw, OpenCode, Codex CLI, and Claude Code by helping add or remove models and providers, change defaults, and update supported JSON or TOML config files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkuiwu](https://clawhub.ai/user/mkuiwu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI tool users use this skill to convert requests for local AI tool configuration changes into supported script commands for OpenClaw, OpenCode, Codex CLI, and Claude Code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist API keys or auth tokens in local AI tool configuration files. <br>
Mitigation: Verify the exact target file and credential values before approving writes, prefer scoped or replaceable keys, and protect or delete backup files that may contain old secrets. <br>
Risk: Provider URLs, model IDs, auth-file replacements, and memory-search settings can change future agent behavior. <br>
Mitigation: Review each proposed provider, model, authentication, and memory-search change before execution, and use summary commands after edits to confirm the resulting configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mkuiwu/ai-config-admin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses bundled scripts to write supported local AI configuration files and create same-directory backups before writes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
