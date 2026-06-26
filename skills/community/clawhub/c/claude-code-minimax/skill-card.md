## Description: <br>
Configures Claude Code to use the MiniMax-M2.5 API through cc-switch, manual Claude settings, or VS Code extension settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[L1-M1ng](https://clawhub.ai/user/L1-M1ng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill as a setup guide for routing Claude Code requests to MiniMax-M2.5 and configuring related Claude Code or VS Code environment settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup requires storing a MiniMax API key in local Claude Code or VS Code configuration. <br>
Mitigation: Use a dedicated or limited API key where possible, keep configuration files out of source control, and avoid sharing logs or files that expose secrets. <br>
Risk: The guide routes Claude Code traffic to MiniMax rather than Anthropic's default API endpoint. <br>
Mitigation: Install only if you are comfortable sending Claude Code requests to MiniMax and review the configured base URL before use. <br>
Risk: The recommended cc-switch workflow depends on an external configuration tool. <br>
Mitigation: Review cc-switch before installing it and only apply Claude Code configurations in folders you control and trust. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/L1-M1ng/claude-code-minimax) <br>
- [MiniMax platform](https://platform.minimaxi.com) <br>
- [Claude Code documentation](https://docs.claude.com) <br>
- [cc-switch GitHub repository](https://github.com/farion1231/cc-switch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown setup guide with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local API key handling guidance and troubleshooting commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
