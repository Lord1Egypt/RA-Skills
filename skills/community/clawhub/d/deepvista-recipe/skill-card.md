## Description:

DeepVista Recipe: Manage structured executable workflows (Recipes) and run them via the AI agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingconan](https://clawhub.ai/user/jingconan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list, inspect, run, export, discover, and install DeepVista Recipe workflows through the DeepVista CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running a remote Recipe may let the agent take broad actions and update DeepVista account context.

Mitigation: Review the Recipe with `deepvista recipe get` before running it, use trusted Recipe sources, and require explicit user confirmation before run or install commands.

Risk: Recipe inputs and runs may involve sensitive user context.

Mitigation: Avoid providing sensitive input unless it is necessary for the workflow and appropriate for the DeepVista account being used.

Risk: The skill installs the DeepVista CLI package without pinning a package version.

Mitigation: Install and run the CLI in a restricted environment, and pin or review the package version through local dependency controls when possible.

## Reference(s):

- [DeepVista CLI Homepage](https://cli.deepvista.ai)
- [ClawHub Skill Page](https://clawhub.ai/jingconan/skills/deepvista-recipe)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline bash commands and DeepVista CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recipe run output streams as NDJSON from the DeepVista CLI.]

## Skill Version(s):

0.1.0-alpha.21 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
