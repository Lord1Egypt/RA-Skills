## Description: <br>
Provides an Agent Reach 1.3.0 installation and configuration workflow with channel setup, verification, and troubleshooting for OpenClaw, Claude Code, and generic AI agent environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pyh-pan](https://clawhub.ai/user/pyh-pan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to install and configure Agent Reach, enable core content channels, validate the local environment, and troubleshoot common setup issues in OpenClaw, Claude Code, or similar agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow uses unpinned remote installation code and the --break-system-packages pip option. <br>
Mitigation: Review install.sh and the Agent Reach source before installing, pin a release or commit where possible, and prefer a virtual environment or pipx for local installation. <br>
Risk: Proxy and cookie examples can expose credentials if pasted into shell history, logs, screenshots, or shared terminals. <br>
Mitigation: Use placeholder values in shared materials and handle real cookies, proxy passwords, and API credentials through private shell sessions or a secret manager. <br>


## Reference(s): <br>
- [Agent Reach Setup on ClawHub](https://clawhub.ai/pyh-pan/agent-reach-setup) <br>
- [Publisher profile: pyh-pan](https://clawhub.ai/user/pyh-pan) <br>
- [Agent Reach repository](https://github.com/Panniantong/agent-reach) <br>
- [Agent Reach issues](https://github.com/Panniantong/agent-reach/issues) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation, channel configuration, environment verification, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
