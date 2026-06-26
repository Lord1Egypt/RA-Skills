## Description: <br>
macOS service persistence and reboot recovery for managing a three-tier LaunchAgent, tmux bootstrap, and wrapper daemon architecture so services can recover after restart. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darwin7381](https://clawhub.ai/user/darwin7381) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan, configure, and diagnose macOS services that should restart after reboot through LaunchAgents, tmux bootstrap sessions, and wrapper daemons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep an unattended Telegram-connected Claude agent running with permission checks bypassed. <br>
Mitigation: Remove permission-bypass flags, restrict Telegram access, and require human review before deploying any persistent agent service. <br>
Risk: Bundled examples include hard-coded personal paths and service names. <br>
Mitigation: Replace personal paths and services with environment-specific values before installation. <br>
Risk: LaunchAgents and tmux wrappers can expose or restart development services unintentionally. <br>
Mitigation: Bind development servers to localhost unless exposure is intentional and verify unload procedures for any LaunchAgents created. <br>
Risk: Auto-confirming trust prompts can approve a workspace without explicit review. <br>
Mitigation: Disable automatic trust confirmation and perform trust decisions manually. <br>


## Reference(s): <br>
- [Auto Reboot Recovery on ClawHub](https://clawhub.ai/darwin7381/auto-reboot-recovery) <br>
- [Bootstrap Script Template](references/bootstrap-template.md) <br>
- [LaunchAgent Plist Template](references/launchagent-template.md) <br>
- [Service Registry Specification](references/registry-spec.md) <br>
- [Wrapper Daemon Script Template](references/wrapper-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands, plist examples, JSON registry examples, and script snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for macOS LaunchAgent and tmux-based service recovery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
