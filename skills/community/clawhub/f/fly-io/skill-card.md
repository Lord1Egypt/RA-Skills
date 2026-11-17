## Description:

Deploy and manage applications on Fly.io using the flyctl CLI and Machines API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dwhite-oss](https://clawhub.ai/user/dwhite-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy, inspect, scale, and administer Fly.io applications, machines, secrets, one-off shell commands, and Fly Postgres databases through flyctl and the Machines API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deploy, scaling, secret, shell, stop, and destroy commands can affect production Fly.io applications.

Mitigation: Before executing mutating commands, confirm the exact app name, environment, machine ID, and expected production impact.

Risk: Secrets and database attachment commands can alter runtime configuration.

Mitigation: Review the target application and secret or database name before setting, unsetting, or attaching resources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dwhite-oss/skills/fly-io)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires flyctl to be installed and authenticated before commands can be used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
