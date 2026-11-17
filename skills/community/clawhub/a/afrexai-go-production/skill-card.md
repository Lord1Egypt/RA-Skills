## Description:

Provides Go production engineering guidance for architecture, error handling, concurrency safety, testing, observability, configuration, CI/CD, deployment, performance, and security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to review, scaffold, and harden Go services for production readiness across architecture, reliability, observability, security, testing, and deployment workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or copied profiling and debug endpoint examples could expose sensitive operational data if published on an unprotected network.

Mitigation: Bind pprof and debug endpoints to localhost or protected admin networks before using the guidance in production.

Risk: Unpinned CI or tooling examples can drift over time and produce inconsistent build or scan results.

Mitigation: Pin tool versions in CI and review version updates through the normal release process.

Risk: Structured logging examples may be adapted in ways that record direct identifiers or sensitive fields.

Mitigation: Apply the organization's logging policy and avoid direct identifiers unless explicitly required and protected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-go-production)
- [Publisher profile](https://clawhub.ai/user/1kalin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Go code examples, shell commands, checklists, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include production-readiness scoring, code review findings, project structure recommendations, CI/CD examples, and operational checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
