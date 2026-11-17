## Description:

Deploy and manage applications on Creek via the Creek CLI, including init, deploy, status, projects, deployments, rollback, environment variables, custom domains, and dev server workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linyiru](https://clawhub.ai/user/linyiru)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Creek to deploy, configure, troubleshoot, and manage web applications through the Creek CLI, including rollbacks, environment variables, custom domains, and preview sandboxes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect live deployments, environment variables, and custom domains, and it recommends using --yes to skip prompts.

Mitigation: Require explicit user confirmation before rollback, displaying or removing environment values, changing domains, or running any command with --yes.

Risk: The skill depends on the Creek CLI and a CREEK_TOKEN for authenticated workflows.

Mitigation: Verify the Creek CLI package source and version before use, keep tokens out of logs, and run the CLI without elevated privileges.

## Reference(s):

- [Creek Skill on ClawHub](https://clawhub.ai/linyiru/skills/creek)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Creek CLI JSON output and breadcrumbs to guide next actions.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
