## Description: <br>
Define multi-container applications with proper dependency handling, networking, and volume management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform engineers use this skill as a Docker Compose reference for service readiness, health checks, volume handling, resource limits, build context hygiene, override files, profiles, and environment variable precedence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker Compose commands can delete persistent application data when volume-removal flags are used. <br>
Mitigation: Review destructive Compose commands before execution and confirm whether named or anonymous volumes should be preserved. <br>
Risk: Compose files and build contexts can expose secrets or environment-specific settings through environment variables, host-mounted paths, or missing .dockerignore entries. <br>
Mitigation: Inspect environment files, host mounts, override files, and build context contents before applying generated configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/docker-compose) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline YAML and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing Docker Compose recommendations and command snippets; review destructive commands and environment-specific configuration before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
