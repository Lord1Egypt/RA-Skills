## Description:

Business module engineer skill for module structure, controllers, menus, setup flows, and bounded feature delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build or modify WelineFramework business modules, including module-local controllers, views, menus, setup flows, and bounded feature work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide code changes inside Weline business modules, so incorrect guidance could affect module behavior.

Mitigation: Keep changes inside the owning module, run focused validation on the changed path, and review results before deployment.

Risk: Setup or route-refresh commands may be needed for schema, setup, or controller routing changes.

Mitigation: Run setup or route-refresh commands only when the module change requires them and capture the command evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiweline/skills/business-module-development)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with code and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include module-local implementation changes, setup or route refresh evidence, and validation notes.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
