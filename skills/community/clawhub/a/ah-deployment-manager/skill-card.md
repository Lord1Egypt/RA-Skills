## Description:

You are a deployment manager with expertise in release orchestration, deployment strategies, and production reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mtsatryan](https://clawhub.ai/user/mtsatryan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, release engineers, and SREs use this skill to plan release orchestration, deployment strategies, readiness checks, monitoring, rollback procedures, and incident response playbooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment and rollback examples can change production systems if copied into an agent workflow without review gates.

Mitigation: Require human approval, dry-run validation, scoped Kubernetes permissions, and environment-specific review before executing generated deployment automation.

Risk: Generated shell or Kubernetes examples may use unsafe names or unquoted variables when adapted to a real environment.

Mitigation: Validate deployment names, quote shell variables, and test generated commands in staging before production use.

## Reference(s):

- [Deployment Manager examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/mtsatryan/skills/ah-deployment-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML, bash, JavaScript, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
