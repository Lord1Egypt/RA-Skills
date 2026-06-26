## Description: <br>
Generate production-grade docker-compose.yml for any project. Includes health checks for every service, network segmentation (frontend/backend/db), resource limits, log rotation, restart policies, secrets management, and backup volumes. Stack-agnostic - works with Node.js, Python, Go, Java, Ruby, PHP, or any Dockerized app. Use when the user says 'docker compose', 'production compose', 'dockerize', 'containerize', or needs a production-ready Compose file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llcsamih](https://clawhub.ai/user/llcsamih) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate or upgrade production Docker Compose configurations for Dockerized applications. It helps detect stacks and dependencies, create compose and environment example files, and validate the result with Docker Compose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may scan project and environment configuration files to infer ports, dependencies, and variables. <br>
Mitigation: Use it only on repositories where that inspection is acceptable, and avoid providing real secrets when possible. <br>
Risk: Generated production Compose files can affect network exposure, persistence, resource limits, and secret handling. <br>
Mitigation: Review docker-compose.yml and .env.example before running them, then validate with docker compose config. <br>
Risk: Broad activation phrases such as dockerize or containerize may invoke the skill when the user needs a different deployment target. <br>
Mitigation: Confirm Docker Compose is the intended deployment format, especially when Kubernetes or managed container platforms are in scope. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/llcsamih/compose-prod) <br>
- [Publisher profile](https://clawhub.ai/user/llcsamih) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with YAML, env-file, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify docker-compose.yml, .env.example, optional secrets directory guidance, and validation instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
