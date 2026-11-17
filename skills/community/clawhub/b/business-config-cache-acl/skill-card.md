## Description:

Business module engineer skill for env config, cache usage, backend menu wiring, and module-level permission integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiweline](https://clawhub.ai/user/aiweline)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when implementing Weline business-module environment configuration, cache wrappers, backend menus, and module-level permission wiring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Operational validation commands such as environment installation or setup refresh can affect the target Weline environment.

Mitigation: Confirm the target environment and review expected changes before running env, setup, or route refresh commands.

Risk: Backend menu visibility and controller permission wiring can become inconsistent if updated separately.

Mitigation: Update backend menus and permission annotations together, then verify menu visibility and controller access through the intended backend path.

## Reference(s):


## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance, markdown]

**Output Format:** [Markdown guidance with code, configuration, and shell command recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include validation evidence and documentation notes for changed admin or runtime behavior.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
