## Description: <br>
Claw Desktop Pet provides setup and usage guidance for an Electron-based desktop AI assistant with fault tolerance, auto-restart, performance monitoring, voice interaction, logging, and resource optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kk43994](https://clawhub.ai/user/kk43994) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install, configure, run, and test a desktop AI assistant with voice notifications and local health monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Desktop assistant setup can carry normal supply-chain risk through the referenced repository and dependency manifests. <br>
Mitigation: Review the referenced repository and dependency manifests before installing or running setup commands. <br>
Risk: An always-on desktop app with auto-restart may continue running longer than intended. <br>
Mitigation: Confirm how to stop the app or disable auto-restart before deployment. <br>
Risk: Local bridge exposure can expand risk if it is not limited to the local machine. <br>
Mitigation: Keep the OpenClaw bridge bound to localhost and avoid running the app as administrator. <br>
Risk: The artifact documentation is primarily Chinese, which can lead to setup mistakes for non-Chinese readers. <br>
Mitigation: Translate the documentation before running setup commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kk43994/claw-desktop-pet) <br>
- [Project README](https://github.com/kk43994/claw-desktop-pet#readme) <br>
- [Release Notes v1.3.0](https://github.com/kk43994/claw-desktop-pet/blob/master/RELEASE-v1.3.0.md) <br>
- [Technical Documentation](https://github.com/kk43994/claw-desktop-pet/tree/master/docs) <br>
- [Issues](https://github.com/kk43994/claw-desktop-pet/issues) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local setup commands, configuration values, usage examples, log inspection commands, and test commands.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and artifact changelog, released 2026-02-07) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
