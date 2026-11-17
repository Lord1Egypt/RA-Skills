## Description:

Use Factory AI's droid CLI for software engineering tasks. Supports interactive mode, exec mode, MCP servers, and plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mitchellbernstein](https://clawhub.ai/user/mitchellbernstein)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to operate Factory AI's Droid CLI for feature development, debugging, refactoring, code review, git operations, deployment, MCP server management, and plugin workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Droid can make code, git, and deployment changes that may be incorrect or unintended.

Mitigation: Use reviewed branches or sandboxes, inspect diffs before commits or deployments, and keep human approval in the workflow.

Risk: The --force option may auto-apply changes without normal confirmation.

Mitigation: Avoid --force for routine work and reserve it for reviewed, low-risk tasks.

Risk: MCP servers, plugins, and model providers extend the CLI's behavior and trust boundary.

Mitigation: Install only trusted providers, verify MCP/plugin names and publishers before adding them, and remove unneeded integrations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command examples, with optional JSON output from the Droid CLI when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require the droid binary and Factory authentication through CLI login or FACTORY_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
