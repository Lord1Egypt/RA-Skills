## Description: <br>
Chezmoi helps agents manage dotfiles through interactive diff review, template consolidation, cross-platform compatibility checks, environment validation, and MCP server synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drumrobot](https://clawhub.ai/user/drumrobot) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to review and apply chezmoi-managed dotfile changes, consolidate repeated templates, keep configurations portable across macOS and Windows, and synchronize MCP server settings across supported apps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SourceGit helper can launch Claude Code with permission safeguards disabled and automatic session resume. <br>
Mitigation: Inspect bin/claude-source.sh before use, remove --dangerously-skip-permissions unless explicitly required, and avoid automatic session resume when handling sensitive repositories. <br>
Risk: Dotfile and MCP synchronization can propagate secrets or sensitive tokens into managed files that may be synced or committed. <br>
Mitigation: Keep secret tokens out of plaintext dotfiles, review chezmoi diff before applying changes, and verify MCP configuration files before committing or sharing them. <br>
Risk: Chezmoi apply operations can overwrite local application configuration. <br>
Mitigation: Run chezmoi diff first and apply only files explicitly approved through the per-file review workflow. <br>


## Reference(s): <br>
- [Chezmoi Skill Page](https://clawhub.ai/drumrobot/chezmoi) <br>
- [Publisher Profile](https://clawhub.ai/user/drumrobot) <br>
- [Apply Guide](apply.md) <br>
- [Template Consolidation Guide](consolidate.md) <br>
- [Cross-Platform Guide](cross-platform.md) <br>
- [Doctor Guide](doctor.md) <br>
- [MCP Sync Guide](mcp-sync.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include per-file approval prompts, diff summaries, and follow-up verification commands.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release evidence and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
