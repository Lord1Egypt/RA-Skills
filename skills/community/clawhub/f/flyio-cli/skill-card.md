## Description:

Helps agents use Fly.io's flyctl CLI to inspect, deploy, debug, and safely operate Fly.io applications and Postgres resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justinburdett](https://clawhub.ai/user/justinburdett)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to guide Fly.io diagnostics, deployments, GitHub Actions setup, preview environments, and Rails/Docker build troubleshooting while requiring approval for state-changing operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fly.io operations can change production application state, secrets, scaling, machines, volumes, or databases.

Mitigation: Use read-only diagnostics first and require explicit user approval before any state-changing operation.

Risk: SSH commands and deploy workflows can execute code in live Fly.io environments.

Mitigation: Confirm the target app and intended command before execution, and capture diagnostic output for review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/justinburdett/skills/flyio-cli)
- [Safety Policy](references/safety.md)
- [Rails + Docker Builds on Fly](references/rails-docker-builds.md)
- [Fly + GitHub Actions](references/github-actions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostics are preferred first; state-changing Fly.io operations require explicit user approval.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
