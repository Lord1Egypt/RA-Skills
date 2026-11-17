## Description:

Deploy and manage the EVEZ-OS infrastructure with seven consciousness microservices, an API gateway, Terraform mesh support, Docker Compose orchestration, and an append-only event spine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run, test, inspect, and manage the EVEZ-OS Firmament microservice stack and its supporting Terraform workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated network APIs may allow unintended access to service state, event data, and control endpoints.

Mitigation: Run only in an isolated development environment unless authentication is added and backend ports are bound to localhost or an internal Docker network.

Risk: Client-controlled Python evaluation in the invariant engine can execute unsafe expressions.

Mitigation: Remove or replace the eval-based invariant engine before exposing the stack beyond a trusted local environment.

Risk: Broad mutable event and state endpoints can be abused or overloaded.

Mitigation: Add input limits, request validation, and rate limits before shared or public use.

Risk: Terraform targets can create, modify, or destroy cloud infrastructure.

Mitigation: Review Terraform plans, variables, credentials, and destroy/apply targets before execution.

## Reference(s):

- [Evez Firmament ClawHub Skill Page](https://clawhub.ai/evezart/skills/evez-firmament)
- [evezart Publisher Profile](https://clawhub.ai/user/evezart)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, code references, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include deployment, testing, health-check, Docker Compose, and Terraform command guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
