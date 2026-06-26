## Description: <br>
Automates deployment of FastapiAdmin in WSL2 Ubuntu, including dependency setup, backend and frontend initialization, Nginx routing fixes, host access, and SSL configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bamboo-art](https://clawhub.ai/user/bamboo-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to deploy FastapiAdmin on Windows machines through WSL2 Ubuntu, with commands and configuration for local services, frontend builds, Nginx routing, and host access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment guidance can make broad privileged system changes in WSL2, including package installation, service changes, and Nginx replacement. <br>
Mitigation: Use a fresh or disposable WSL2 Ubuntu environment, or back up Nginx and confirm no existing local services depend on it before running privileged commands. <br>
Risk: Default local credentials and cloned dependency trees may be unsuitable for a durable or shared environment. <br>
Mitigation: Review the cloned repositories and dependency files, replace the default database password, and keep secrets out of committed configuration files. <br>
Risk: Network and SSL settings are environment-specific and can break access when the WSL2 IP changes or a self-signed certificate is used. <br>
Mitigation: Confirm the current WSL2 IP, rebuild frontend environment values when it changes, and prefer reviewed HTTP or trusted certificate settings for local access. <br>


## Reference(s): <br>
- [FastapiAdmin WSL2 troubleshooting guide](references/troubleshooting.md) <br>
- [FastapiAdmin source repository](https://gitee.com/fastapiadmin/FastapiAdmin.git) <br>
- [FastDocs source repository](https://gitee.com/fastapiadmin/FastDocs.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and Nginx configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands that may require sudo and environment-specific WSL2 IP values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
