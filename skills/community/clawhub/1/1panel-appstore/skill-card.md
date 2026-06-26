## Description: <br>
Create 1Panel appstore/local-app installation packages for Dockerized applications from official repositories, Docker images, docker-compose.yml files, or a prepared app spec. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1panel](https://clawhub.ai/user/1panel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to convert Docker-based application sources, Compose files, Docker images, or prepared app specs into 1Panel local app packages for review and testing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated packages may expose ports, mount host paths, set Docker service options, include secrets, or create init scripts that affect the target 1Panel host. <br>
Mitigation: Install this only if you intend to generate 1Panel local app packages. Before installing any generated package in 1Panel, review its docker-compose.yml, data.yml, exposed ports, host mounts, image provenance, secrets, and especially any scripts/init.sh content; test first on a non-production host. <br>
Risk: Packaging from incomplete or unofficial Docker installation evidence can produce incorrect images, ports, volumes, environment variables, or runtime user settings. <br>
Mitigation: Use the skill only with official repositories, official documentation, user-approved third-party images, or a prepared app spec, and preserve source evidence for Docker installation details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1panel/1panel-appstore) <br>
- [Publisher profile](https://clawhub.ai/user/1panel) <br>
- [Source Policy](references/source-policy.md) <br>
- [1Panel Appstore Format](references/appstore-format.md) <br>
- [Intermediate App Spec](references/appspec.md) <br>
- [Review Checklist](references/review-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown response plus generated 1Panel app package files and JSON/YAML configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports package path, generated version, source evidence, warnings, assumptions, and local test target.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
