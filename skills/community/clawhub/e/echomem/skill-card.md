## Description: <br>
Guides users through installing, configuring, using, and troubleshooting the EchoMemory Cloud OpenClaw Plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangshi0512](https://clawhub.ai/user/zhangshi0512) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to install, configure, operate, and troubleshoot the EchoMemory Cloud OpenClaw plugin, including local UI access, cloud sync, mode switching, and recovery checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: EchoMemory setup may generate an API key and store it locally in ~/.openclaw/.env. <br>
Mitigation: Restrict file permissions, avoid syncing or committing the env file, and rotate the key if the machine is shared or compromised. <br>
Risk: The local UI can show a wider set of local OpenClaw markdown files than the cloud sync importer uploads. <br>
Mitigation: Review local workspace files and the configured memoryDir before syncing, and use local-only mode when cloud sync is not intended. <br>


## Reference(s): <br>
- [EchoMemory on ClawHub](https://clawhub.ai/zhangshi0512/echomem) <br>
- [OpenClaw Marketplace listing](https://openclawdir.com/plugins/echomemory-ArQh3g) <br>
- [NPM package](https://www.npmjs.com/package/@echomem/openclaw-memory) <br>
- [EchoMemory API key management](https://www.iditor.com/api) <br>
- [Initial setup](references/initial-setup.md) <br>
- [Normal usage](references/normal-usage.md) <br>
- [Mode switching](references/mode-switching.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command routing suggestions for EchoMemory tools and local/cloud mode choices.] <br>

## Skill Version(s): <br>
0.2.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
