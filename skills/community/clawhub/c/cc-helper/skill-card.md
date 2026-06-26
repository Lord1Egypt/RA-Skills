## Description: <br>
One-click environment check and multi-provider setup for Claude Code that detects Node.js, Git, npm, installs or verifies the Claude Code CLI, configures supported providers, generates settings, and verifies the setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sallyface0](https://clawhub.ai/user/sallyface0) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to configure Claude Code with third-party Anthropic-compatible API providers, choose provider-specific settings, and verify that the local CLI environment works across Windows, macOS, Linux, and WSL2. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide users through system-changing setup steps, including installing software and writing Claude Code provider settings. <br>
Mitigation: Review installation commands and the generated `.claude/settings.local.json` before applying them. <br>
Risk: Provider setup may involve API credentials and commands that fetch or execute remote installer scripts. <br>
Mitigation: Keep credentials out of version control, review any command that pipes remote content into a shell, and back up credential files instead of deleting them outright. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sallyface0/cc-helper) <br>
- [Installation Guide](references/install-guide.md) <br>
- [Provider Configuration Matrix](references/provider-table.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command blocks and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose environment variables and Claude Code settings for selected third-party providers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
