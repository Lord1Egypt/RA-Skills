## Description: <br>
Create and manage Docker sandboxed VM environments for safe agent execution, including untrusted code exploration, package testing, isolated agent workloads, and network proxy controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LucasSeeley](https://clawhub.ai/user/LucasSeeley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to create Docker Desktop sandbox VMs for running untrusted code, exploring packages, isolating agent workloads, and controlling outbound network access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mounted workspace files can be changed by commands or agents running inside the sandbox. <br>
Mitigation: Use disposable project copies for untrusted code and avoid mounting sensitive directories. <br>
Risk: Sandboxed workloads may still make outbound network requests when network policy is permissive. <br>
Mitigation: Prefer deny-by-default network proxy rules and allow only the domains required for the task. <br>
Risk: Remove and reset commands can destroy sandbox state. <br>
Mitigation: Save or export any needed work before running remove or reset commands. <br>


## Reference(s): <br>
- [Docker Desktop Sandbox Documentation](https://docs.docker.com/desktop/features/sandbox/) <br>
- [ClawHub Skill Page](https://clawhub.ai/LucasSeeley/docker-sandbox-lucas) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance for Docker Desktop sandbox operations; requires Docker Desktop 4.49+ with the docker sandbox plugin.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
