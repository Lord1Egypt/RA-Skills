## Description: <br>
Executes untrusted code or commands in a secure, isolated Docker environment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assix](https://clawhub.ai/user/assix) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to identify untrusted command execution tasks and route them to a Docker-based sandbox for isolated execution and output review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is described as a sandbox, but the security evidence says the runner script and Dockerfile are missing, so the package cannot prove or provide the claimed isolation. <br>
Mitigation: Do not rely on it for untrusted code until those files are provided and audited for no network, dropped capabilities, non-root execution, seccomp use, no host-sensitive mounts, and disposable containers. <br>
Risk: The skill is intended to execute untrusted commands, which can expose host systems if sandboxing is incomplete or misconfigured. <br>
Mitigation: Review commands before execution and run them only inside an audited Docker configuration with dropped capabilities, disabled networking, a non-root user, seccomp filtering, no sensitive host mounts, and disposable containers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/assix/agent-securitysandbox) <br>
- [Docker installation documentation](https://docs.docker.com/get-docker/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and sandbox stdout/stderr text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker; claimed sandbox behavior depends on the missing runner script and Dockerfile being supplied and audited.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
