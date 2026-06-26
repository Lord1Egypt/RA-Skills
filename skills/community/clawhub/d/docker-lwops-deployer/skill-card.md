## Description: <br>
Automates local Docker deployment and management of a LwOps 8.1 monitoring container, including Docker setup, architecture-aware image selection, port allocation, and deployment status output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lerwee](https://clawhub.ai/user/lerwee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy, redeploy, inspect, and troubleshoot a local LwOps 8.1 Docker container for development, testing, or containerized service management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad host privileges to install Docker and manage containers. <br>
Mitigation: Review before installing on a real machine and avoid applying NOPASSWD: ALL sudoers guidance; grant only the minimum privileges needed. <br>
Risk: The deployment uses privileged containers and includes container or image cleanup commands. <br>
Mitigation: Avoid privileged containers unless the requirement is understood, and inspect deploy and cleanup commands before allowing removal of containers, images, volumes, or local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lerwee/docker-lwops-deployer) <br>
- [Project homepage](https://github.com/lwops/docker-lwops-deployer) <br>
- [LwOps website](https://www.lwops.cn) <br>
- [Docker documentation](https://docs.docker.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON status objects with deployment details, access URLs, and error suggestions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include container name, image, architecture, host ports, cgroup mode, timestamps, and remediation suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
