## Description: <br>
Remotely install and configure Claude Code CLI on a target machine via SSH. Requires the user to explicitly provide a target address (user@host) and password. The skill never stores, logs, or transmits credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lingmaker9](https://clawhub.ai/user/lingmaker9) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to remotely install Claude Code CLI on a Linux target machine over SSH after the user supplies an explicit target address and password. It guides dependency checks, package installation, npm registry configuration, Claude Code installation, onboarding configuration, and manual API-key setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run high-impact SSH commands and privileged dependency installation on a remote machine. <br>
Mitigation: Use it only on machines you control, review each command before execution, and require explicit confirmation before any sudo action. <br>
Risk: The dependency path can execute a downloaded setup script with sudo and change npm package-source settings. <br>
Mitigation: Confirm the setup script, registry, mirror choices, and package version against trusted sources before installation. <br>
Risk: The skill modifies Claude configuration by setting the onboarding flag in the target user's home directory. <br>
Mitigation: Review or back up any existing Claude configuration before writing changes, especially on shared or production accounts. <br>
Risk: The workflow relies on a user-provided SSH password for the remote session. <br>
Mitigation: Provide credentials only for the current session, avoid logging or storing them, and prefer a controlled account with the minimum required privileges. <br>
Risk: The API-key setup guidance includes a placeholder package-source choice. <br>
Mitigation: Replace placeholder API-key setup and package-source choices with trusted, organization-approved instructions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lingmaker9/claude-installer) <br>
- [Server-resolved source repository](https://github.com/LingMaker9/claude-installer) <br>
- [NodeSource Node.js setup script referenced by the skill](https://deb.nodesource.com/setup_20.x) <br>
- [npm mirror registry referenced by the skill](https://registry.npmmirror.com/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and step-by-step operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an explicit SSH target address and password; stops for missing inputs, unsupported targets, sudo confirmation, or unexpected states.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
