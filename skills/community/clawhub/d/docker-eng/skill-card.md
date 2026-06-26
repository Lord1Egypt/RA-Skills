## Description: <br>
Deep Docker workflow-image design, multi-stage builds, security, runtime config, health checks, and operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to containerize applications, improve Dockerfile structure, harden images, configure runtime behavior, define health checks, and debug container behavior in CI and production. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dockerfile edits, image pushes, registry logins, or production deployment changes proposed while using this skill can affect real systems. <br>
Mitigation: Review proposed changes before execution, test them in non-production environments, scan resulting images, and confirm registry or orchestrator targets before applying changes. <br>
Risk: Container configuration guidance can accidentally introduce secrets into image layers or runtime manifests if applied carelessly. <br>
Mitigation: Keep secrets out of Dockerfiles and image layers, inject secrets at runtime through approved secret stores, and inspect build context and .dockerignore entries before building images. <br>


## Reference(s): <br>
- [Docker Eng on ClawHub](https://clawhub.ai/mikeclaw007/docker-eng) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Dockerfile, shell command, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces review checklists and implementation guidance for Docker workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
