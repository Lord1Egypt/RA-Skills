## Description: <br>
Use the Fly.io flyctl CLI for deploying and operating apps on Fly.io, starting with read-only diagnostics and requiring explicit approval before deploys, SSH exec, secrets, scaling, machines, volumes, or Postgres changes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justinburdett](https://clawhub.ai/user/justinburdett) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to deploy, inspect, debug, and safely operate Fly.io applications and Fly Postgres resources with flyctl. It is especially useful for diagnosing deploy/build/runtime failures, setting up GitHub Actions deploys or previews, and proposing operational commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: State-changing Fly.io operations can affect deployed apps, secrets, databases, volumes, machines, or production availability. <br>
Mitigation: Require explicit user approval after reviewing the exact app name, account, command, and expected impact before deploys, SSH commands, secrets changes, scaling, machine, volume, or Postgres operations. <br>
Risk: Fly.io API tokens can grant access to infrastructure resources. <br>
Mitigation: Store FLY_API_TOKEN only as a protected, least-privilege secret and avoid exposing token values in logs or generated output. <br>


## Reference(s): <br>
- [Safety policy](references/safety.md) <br>
- [Fly + GitHub Actions](references/github-actions.md) <br>
- [Rails + Docker builds on Fly](references/rails-docker-builds.md) <br>
- [ClawHub skill page](https://clawhub.ai/justinburdett/flyio-cli) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostics are preferred before proposing state-changing operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
