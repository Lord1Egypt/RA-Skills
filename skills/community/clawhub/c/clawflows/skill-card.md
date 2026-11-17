## Description:

Search, install, and run multi-skill automations from clawflows.com. Combine multiple skills into powerful workflows with logic, conditions, and data flow between steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cluka-399](https://clawhub.ai/user/cluka-399)

### License/Terms of Use:


## Use Case:

Developers and automation users use this skill to discover, install, check, run, schedule, and publish ClawFlows multi-skill automations that coordinate capabilities across other skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installed automations are mutable third-party workflows that may use sensitive local capabilities.

Mitigation: Review each automation YAML and the requested capabilities before running it, especially workflows that access email, calendars, databases, or scheduling.

Risk: The documented global npm install is not pinned to a reviewed package version.

Mitigation: Review the clawflows npm package before installation and prefer a pinned or otherwise verified version when operating in a controlled environment.

Risk: Running an automation can execute actions across multiple skills.

Mitigation: Use the documented --dry-run option first and run workflows with only the permissions needed for the intended task.

## Reference(s):

- [Clawflows on ClawHub](https://clawhub.ai/cluka-399/skills/clawflows)
- [ClawFlows Registry](https://clawflows.com)
- [clawflows npm package](https://www.npmjs.com/package/clawflows)
- [ClawFlows registry repository listed by the skill](https://github.com/Cluka-399/clawflows-registry)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may install or run workflow YAML files and can use a dry-run mode before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
