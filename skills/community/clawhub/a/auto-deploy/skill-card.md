## Description: <br>
Automates Git project deployment by pulling code, building, and deploying via SSH to Linux servers with backup and health checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjm1226](https://clawhub.ai/user/zjm1226) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy Git-backed Node.js, Java, or mixed projects to Linux servers over SSH. It supports pulling code, building artifacts, uploading releases, restarting services, running health checks, and rolling back from backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes real-looking Git and server credentials and root-oriented SSH deployment configuration. <br>
Mitigation: Rotate exposed credentials, remove hardcoded secrets, use secret storage or environment variables, and replace root access with a least-privilege deploy user before use. <br>
Risk: Deployment, restart, rollback, package installation, SSH key installation, and code push steps can change or damage a live server. <br>
Mitigation: Use only on systems you own, validate deployment paths and target hosts, keep backups enabled, and require explicit approval before any mutating operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zjm1226/auto-deploy) <br>
- [README](artifact/README.md) <br>
- [Deployment configuration guide](artifact/DEPLOY_CONFIG.md) <br>
- [SSH setup guide](artifact/SSH_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, and deployment scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run deployment, rollback, SSH, Git, build, package installation, and service restart commands that require review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
