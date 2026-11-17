## Description: <br>
API Scaffold Gen helps developers generate API project scaffolds, including REST and GraphQL routes, ORM and migration files, DDD layers, microservice templates, OpenAPI artifacts, WebSocket endpoints, Docker files, and CI/CD configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, and platform engineers use this skill to start API projects quickly and standardize framework, domain layering, service, deployment, and automation templates across teams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request broad workspace read, write, and command execution authority. <br>
Mitigation: Run it in a bounded workspace, review proposed file changes, and confirm commands before execution. <br>
Risk: Deployment-oriented generation may touch infrastructure configuration or sensitive project context. <br>
Mitigation: Avoid production credentials, review generated Docker, Kubernetes, and CI/CD files before use, and verify how repository content is handled by the agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/api-scaffold-gen) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated project files, configuration snippets, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write workspace files and propose or run commands when the agent environment permits those tools.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
