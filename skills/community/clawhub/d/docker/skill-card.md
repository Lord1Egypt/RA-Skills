## Description: <br>
Docker containers, images, Compose stacks, networking, volumes, debugging, production hardening, and the commands that keep real environments stable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill for Docker container, image, Compose, networking, volume, debugging, security, and production-hardening guidance. It helps agents propose stable Docker commands and configuration patterns for real environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker cleanup and removal commands can delete containers, images, volumes, build cache, networks, or Compose resources. <br>
Mitigation: Confirm the active Docker context, target resources, and exact command before running prune, volume, compose down, remove, push, or production container operations. <br>
Risk: Production container changes can affect exposed ports, mounted volumes, network reachability, credentials, or host resources. <br>
Mitigation: Review proposed commands and configuration against the intended environment, with special attention to published ports, bind mounts, secrets, privileges, and resource limits. <br>


## Reference(s): <br>
- [Docker skill page](https://clawhub.ai/ivangdavila/docker) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Skill homepage](https://clawic.com/skills/docker) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the docker binary and supports Linux, macOS, and Windows according to release metadata.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
