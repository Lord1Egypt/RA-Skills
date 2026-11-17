## Description:

Automates local Docker deployment of a LwOps Monitor 8.1 container, including Docker setup, architecture selection, port allocation, and cgroup handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lerwee](https://clawhub.ai/user/lerwee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up or inspect a local LwOps Monitor 8.1 Docker environment for development, testing, and container service management. It is intended for hosts where Docker installation, service changes, port publishing, and privileged containers are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or start Docker and modify host container state.

Mitigation: Run it only on an isolated host where Docker service changes are approved, and require explicit user confirmation before deployment.

Risk: The deployed container runs in privileged mode and mounts the host cgroup filesystem.

Mitigation: Avoid shared or sensitive hosts, review the image before use, and restrict execution to environments where privileged containers are acceptable.

Risk: Published container ports may expose the service beyond the intended audience.

Mitigation: Use firewall or network controls to limit access to trusted networks and verify the final port mappings after deployment.

Risk: The remote container image is selected dynamically and documented with latest tags.

Mitigation: Pin and verify the image digest before running the deployment in controlled environments.

Risk: Documentation suggests broad passwordless sudo as a troubleshooting path.

Mitigation: Do not follow NOPASSWD: ALL guidance; grant only the minimum privileges required by local policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lerwee/skills/docker-lwops-deployer)
- [ClawHub publisher profile](https://clawhub.ai/user/lerwee)
- [Project homepage](https://github.com/lwops/docker-lwops-deployer)
- [LwOps website](https://www.lwops.cn)
- [Docker documentation](https://docs.docker.com/)
- [Docker installation documentation](https://docs.docker.com/get-docker/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON status objects with plain-text progress, access URLs, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report container name, image, architecture, host IP, port mappings, cgroup mode, timestamps, errors, and suggested remediation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
