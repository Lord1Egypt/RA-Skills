## Description:

Agent Architecture Designer helps agents select and validate software architecture patterns through prototypes, tests, metrics, and architecture decision records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nntrivi2001](https://clawhub.ai/user/nntrivi2001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide architecture decisions for APIs, services, databases, messaging, and caching. It emphasizes working prototypes, integration tests, load tests, security scans, metrics, and ADRs before recommendations are accepted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose writing prototypes or running commands, tests, scans, or Docker-based checks.

Mitigation: Review proposed changes and commands before applying them to a real project, repository, or infrastructure environment.

Risk: Architecture recommendations can be misleading if accepted without project-specific validation.

Mitigation: Require working prototypes, integration tests, measured performance results, security review, and ADR evidence before treating recommendations as ready for implementation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nntrivi2001/skills/agent-architecture-designer)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with code, configuration, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prototype plans, runnable code, Docker manifests, validation reports, security scan recommendations, ADRs, runbooks, monitoring guidance, and measured architecture tradeoffs.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
