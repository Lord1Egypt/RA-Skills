## Description: <br>
Store and use a sudo password for automated root commands when agent workflows need elevated permissions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stigg86](https://clawhub.ai/user/stigg86) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to configure a helper that can run selected shell commands with sudo in automated agent workflows. It is intended for workflows that require elevated system access, such as installing or restarting system services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a recoverable sudo credential and enables broad unattended root command execution. <br>
Mitigation: Install only for trusted workflows that need this capability; prefer normal sudo prompts, limited sudoers rules for specific commands, or an OS-backed secret store when possible. <br>
Risk: Commands invoked through the helper can make privileged system changes. <br>
Mitigation: Review commands before execution and restrict use to known, necessary administrative actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stigg86/bud-sudo) <br>
- [Skill homepage](https://github.com/stigg86/sudo-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup, status, reset, and sudo command examples for a local shell environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
