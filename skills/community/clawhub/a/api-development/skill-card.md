## Description: <br>
Meta-skill that orchestrates the full API development lifecycle from design through documentation by coordinating specialized skills, agents, and commands into a build workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan, build, test, document, version, and deploy REST, GraphQL, or gRPC APIs through a structured lifecycle workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Downstream implementation, deployment, CI/CD, database, or production API actions may use credentials or affect live systems. <br>
Mitigation: Review downstream skills before use and use scoped credentials for deployment, CI/CD, database, and production API operations. <br>
Risk: Generated API designs, schemas, code, or documentation can encode incorrect security, authorization, error handling, or versioning decisions. <br>
Mitigation: Review generated outputs against the API checklist, run tests, and validate OpenAPI or contract artifacts before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page: api-development](https://clawhub.ai/wpank/api-development) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with checklists, code blocks, generated API artifacts, and implementation steps.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only orchestration skill; no hidden execution, credential collection, persistence, or destructive behavior was reported in the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
