## Description:

Check deployment status of PRs and commits using continuous-deployment MCP and UCS deployer MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajitsingh25](https://clawhub.ai/user/ajitsingh25)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to check whether a GitHub PR, commit, or recent service commit is deployed to staging and production.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries internal GitHub and deployment systems, which may expose deployment status to unauthorized users if installed in the wrong environment.

Mitigation: Install and use it only in workspaces whose users are authorized to access the referenced internal systems.

Risk: Deployment conclusions depend on matching the PR to the correct merge commit and service.

Mitigation: Verify the PR metadata, service name, and merge commit before relying on staging or production status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajitsingh25/skills/check-deployment-status)

## Skill Output:

**Output Type(s):** [guidance, shell commands]

**Output Format:** [Markdown with MCP tool call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authorized access to the referenced internal GitHub and deployment status systems.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
