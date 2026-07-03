## Description: <br>
Install Alibaba Cloud Agent Toolkit end-to-end by verifying and setting up uv, Alibaba Cloud CLI, authentication, CLI plugins, MCP Server Core, bearer token exchange, and the openplugin toolkit install. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare an Alibaba Cloud environment for the Alibaba Cloud Agent Toolkit. It guides prerequisite checks, user-approved local installs, Alibaba Cloud authentication, MCP Server Core setup, bearer-token verification, and final toolkit installation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures Alibaba Cloud tooling and can create or verify cloud-side resources using the user's existing credentials. <br>
Mitigation: Install and run it only when Alibaba Cloud Agent Toolkit setup is expected, and review each proposed install or cloud write command before approving execution. <br>
Risk: The bearer-token check uses a non-standard hardcoded RamOAuth GenerateAccessToken command with an internal scope. <br>
Mitigation: Review the command exactly as presented before allowing it to run, verify it matches the intended Alibaba Cloud setup flow, and confirm the active RAM identity with sts get-caller-identity. <br>
Risk: Some prerequisite installers use pipe-to-shell style commands. <br>
Mitigation: Prefer vendor-documented installers where possible and require explicit user approval before executing any local install command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-agent-toolkit-install) <br>
- [uv installer](https://astral.sh/uv/install.sh) <br>
- [Alibaba Cloud CLI installer](https://aliyuncli.alicdn.com/install.sh) <br>
- [Alibaba Cloud RAM console](https://ram.console.aliyun.com/) <br>
- [Alibaba Cloud RAM applications console](https://ram.console.aliyun.com/applications?activeTab=ThirdParty) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before local installs, CLI plugin installs, cloud-side writes, and final toolkit installation.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
