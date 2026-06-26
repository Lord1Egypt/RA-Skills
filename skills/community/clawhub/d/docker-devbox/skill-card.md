## Description: <br>
Devbox helps agents generate Docker Compose development environments by detecting project type, matching runtime versions, assigning ports, and optionally adding database services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nciae-zyh](https://clawhub.ai/user/nciae-zyh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use Devbox to create isolated Docker-based development environments for existing projects, generate a compose file, resolve port conflicts, and attach local database services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Docker Compose files can expose application and database services with default credentials and mounted environment files. <br>
Mitigation: Review docker-compose.dev.yml before running it, change database and MinIO credentials before shared or network-accessible use, and check exposed ports and env_file entries. <br>
Risk: Bun mode uses a remote installer trust boundary. <br>
Mitigation: Avoid Bun mode unless you accept that trust boundary, or inspect and pin the installer path before use. <br>
Risk: Containers and named Docker volumes can retain dependencies, caches, build artifacts, and service data after use. <br>
Mitigation: Stop and remove containers when finished, and remove the generated Docker volumes when cached or service data should not persist. <br>


## Reference(s): <br>
- [Devbox README](README.md) <br>
- [Docker Compose Templates](references/docker-templates.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/nciae-zyh/docker-devbox) <br>


## Skill Output: <br>
**Output Type(s):** [Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated Docker Compose YAML files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Docker and Docker Compose; generated environments may expose local ports and create named Docker volumes.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
