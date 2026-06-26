## Description: <br>
Docker container lifecycle management, health checks, log analysis, cleanup, compose orchestration, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ericlooi504](https://clawhub.ai/user/ericlooi504) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Docker containers, review logs and health state, manage Docker Compose services, and clean up unused Docker resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Docker cleanup and Compose commands can remove containers, images, networks, volumes, or build cache, which may cause data loss. <br>
Mitigation: Require explicit approval before prune, volume, build-cache, or compose down -v actions; prefer dry-run or inspection commands before destructive cleanup. <br>
Risk: Docker and sudo commands can control host services and affect running workloads. <br>
Mitigation: Review the target container, service, or host action before execution and limit commands to the intended Docker project or container. <br>
Risk: Container logs may contain application secrets, customer data, or other sensitive operational details. <br>
Mitigation: Limit log collection to the needed time range and redact sensitive values before sharing or storing log excerpts. <br>


## Reference(s): <br>
- [Docker Compose Patterns](references/compose-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Docker CLI commands, Docker Compose snippets, health summaries, log-filtering guidance, and cleanup recommendations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
