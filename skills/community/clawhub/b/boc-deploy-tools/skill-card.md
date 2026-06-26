## Description: <br>
博云BOC容器平台 部署工具。整合了部署机初始化和平台部署功能，自动完成从环境初始化到部署验证的全流程。使用场景：用户需要初始化部署机并部署 BOC容器平台时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongruiji](https://clawhub.ai/user/hongruiji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to initialize a deployment host, generate deployment configuration, run BOC container platform installation, and verify Kubernetes node and Pod status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A cleanup command can remove an existing BOC deployment directory if run from the wrong deployment package directory. <br>
Mitigation: Confirm the target host and working directory before execution, and prefer a backup or rename-based cleanup before deleting files. <br>
Risk: The skill performs long-running deployment operations over SSH using privileged credentials. <br>
Mitigation: Run it only on intended deployment hosts, validate input IP addresses and credentials, and monitor logs and process checks during initialization and installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongruiji/boc-deploy-tools) <br>
- [sshpass for Windows release](https://github.com/xhcoding/sshpass-win32/releases/download/v1.0.7/sshpass.exe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands, configuration guidance, status checks, and troubleshooting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes deployment progress checks, log inspection commands, and post-deployment validation guidance] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
