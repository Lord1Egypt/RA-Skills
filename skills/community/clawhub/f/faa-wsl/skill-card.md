## Description:

Automates deployment guidance for FastapiAdmin on Windows WSL2 Ubuntu, covering environment setup, backend and frontend setup, Nginx SPA routing, host access, SSL configuration, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bamboo-art](https://clawhub.ai/user/bamboo-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy FastapiAdmin in a Windows WSL2 Ubuntu environment, including required services, application setup, Nginx configuration, and cross-host browser access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged setup commands can overwrite system web-server configuration or remove existing Nginx site configuration.

Mitigation: Review commands before execution, back up the WSL2 instance and Nginx configuration, and avoid replacing global Nginx files unless the instance is dedicated to this app.

Risk: The documented default database credential is weak for a deployed service.

Mitigation: Generate unique database credentials and update the application environment configuration before exposing the service.

Risk: Unpinned repositories and package installs can change behavior between runs.

Mitigation: Pin repository commits and dependency versions before using the deployment in a shared or production environment.

## Reference(s):

- [FastapiAdmin WSL2 deployment troubleshooting](references/troubleshooting.md)
- [FastapiAdmin source repository](https://gitee.com/fastapiadmin/FastapiAdmin.git)
- [FastDocs source repository](https://gitee.com/fastapiadmin/FastDocs.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, nginx, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that may require privileged execution in WSL2.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
