## Description: <br>
Safely install, uninstall, reinstall, or upgrade the Bamdra OpenClaw memory suite when stale config, existing plugin directories, or partial installs block normal OpenClaw plugin installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bamdra](https://clawhub.ai/user/bamdra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to repair blocked Bamdra memory suite installs, perform upgrades or uninstalls, and preserve OpenClaw configuration integrity through backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill changes OpenClaw configuration and moves Bamdra plugin or skill directories during lifecycle operations. <br>
Mitigation: Confirm the OpenClaw home path and package spec before execution, then keep the generated backup directory until OpenClaw starts and the memory suite works. <br>
Risk: Using the wrong package version or target path can repair or uninstall the wrong Bamdra memory suite installation. <br>
Mitigation: Use the default package only when appropriate, pass an explicit package spec for pinned upgrades, and verify any custom OpenClaw home before running the script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bamdra/bamdra-memory-upgrade-operator) <br>
- [Publisher profile](https://clawhub.ai/user/bamdra) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports backup locations and restart guidance after install, upgrade, or uninstall operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
