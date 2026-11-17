## Description:

Search, install, and run multi-skill automations from clawflows.com. Combine multiple skills into powerful workflows with logic, conditions, and data flow between steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use clawflows to discover, install, inspect, and run portable multi-skill automations that coordinate capabilities such as data access, charts, scheduling, external AI services, and workflow logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automations can download mutable workflow YAML that may invoke sensitive capabilities such as email, calendar, database, external AI access, or local commands.

Mitigation: Review automation YAML before running it, use `clawflows check`, and run `clawflows run --dry-run` before permitting real actions.

Risk: The skill relies on a global npm-installed CLI and a SKILLBOSS_API_KEY for AI-backed automation steps.

Mitigation: Install the CLI only from the intended npm package, protect the API key as a secret, and avoid workflows that request access beyond the intended task.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/abeltennyson/skills/abe-clawflows)
- [ClawFlows registry](https://clawflows.com)
- [clawflows npm package](https://www.npmjs.com/package/clawflows)
- [ClawFlows registry repository](https://github.com/Cluka-399/clawflows-registry)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, YAML, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that install the clawflows CLI, manage automation YAML files, and configure SKILLBOSS_API_KEY.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
