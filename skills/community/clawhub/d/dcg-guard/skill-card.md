## Description: <br>
Hard-blocks dangerous shell commands (rm -rf, git push --force, etc.) before execution via OpenClaw's before_tool_call plugin hook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[StarenseN](https://clawhub.ai/user/StarenseN) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use DCG Guard to add a gateway-level OpenClaw guard that blocks destructive shell commands before execution while allowing ordinary shell activity to pass through. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer runs unpinned remote code for the optional DCG binary. <br>
Mitigation: Inspect the installer first or install a pinned and verified DCG release instead of running curl piped directly to bash. <br>
Risk: The skill installs a persistent gateway-level shell-command guard. <br>
Mitigation: Deploy only in environments where administrators intentionally want command blocking at the OpenClaw gateway level and have verified the disable or uninstall process. <br>
Risk: Advertised enabled and dcgBin configuration controls are not fully implemented in the active code. <br>
Mitigation: Validate behavior in a test OpenClaw environment before relying on those controls in production. <br>


## Reference(s): <br>
- [DCG Guard on ClawHub](https://clawhub.ai/StarenseN/dcg-guard) <br>
- [Dangerous Command Guard](https://github.com/Dicklesworthstone/destructive_command_guard) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [OpenClaw plugin files, shell installer, JSON configuration, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Blocks matched dangerous shell commands through the OpenClaw before_tool_call hook and returns block reasons for destructive or irreversible commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, openclaw.plugin.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
