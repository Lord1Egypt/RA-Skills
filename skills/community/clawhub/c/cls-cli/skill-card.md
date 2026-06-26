## Description: <br>
Command-line tool for managing Tencent Cloud CLS, including log search, topics, alarms, dashboards, machine groups, collectors, LogListener, and general CLS API actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trumphuang](https://clawhub.ai/user/trumphuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to install and configure cls-cli, query Tencent Cloud CLS logs, and manage CLS resources through shortcut commands or raw API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad Tencent Cloud CLS authority, including create, update, delete, and raw API actions. <br>
Mitigation: Use least-privilege or temporary Tencent Cloud credentials and require explicit user confirmation before any create, update, delete, or raw API command is run. <br>
Risk: Tencent Cloud API secrets may be handled through configuration, environment variables, or command examples. <br>
Mitigation: Avoid pasting secrets into chats or command-line flags, prefer controlled environment variables or local config with restricted permissions, and rotate exposed credentials. <br>
Risk: Install and upgrade flows may fetch source or binaries and replace the local cls-cli executable. <br>
Mitigation: Review the install or upgrade command before execution and run it only in an environment where replacing the executable is acceptable. <br>


## Reference(s): <br>
- [ClawHub CLS CLI release page](https://clawhub.ai/trumphuang/cls-cli) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, CLI arguments, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Tencent Cloud CLS read, create, update, delete, install, upgrade, and raw API commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
