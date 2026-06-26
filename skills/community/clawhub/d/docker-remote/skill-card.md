## Description: <br>
Remotely manage Docker Compose instances via SSH, including service lifecycle commands, logs, image updates, and container exec operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elric2011](https://clawhub.ai/user/elric2011) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to administer Docker Compose applications on remote servers over SSH during deployment, monitoring, updates, and debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad remote service-control and command-execution power over SSH. <br>
Mitigation: Use a dedicated non-root deployment user, restrict SSH keys to approved hosts and directories, review deploy-apps.json before use, and require explicit human confirmation for down, restart, update, exec, and custom commands. <br>
Risk: Logs, exec commands, or remote configuration files may expose secrets from Docker environments. <br>
Mitigation: Avoid printing .env files, credentials, or sensitive environment variables, and review command output before storing or sharing it. <br>


## Reference(s): <br>
- [Docker Remote Reference](references/README.md) <br>
- [Command Examples](examples/docker-remote.json) <br>
- [Deployment Configuration Example](examples/deploy-apps.json) <br>
- [ClawHub skill page](https://clawhub.ai/elric2011/docker-remote) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Markdown and command-style text with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured success or failure status, logs, and error context from remote Docker Compose operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
