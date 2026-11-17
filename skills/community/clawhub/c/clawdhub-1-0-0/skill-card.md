## Description:

Use the ClawdHub CLI to search, install, update, and publish agent skills from clawdhub.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djmarkd38](https://clawhub.ai/user/djmarkd38)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to manage ClawdHub CLI workflows for finding, installing, updating, listing, authenticating, and publishing agent skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides registry-management actions that can install, update, or publish skill folders in a workspace.

Mitigation: Use it only in workspaces intended for skill changes, review skill folders before publishing, and understand the impact before forced or bulk updates.

Risk: The workflow depends on a globally installed npm CLI package.

Mitigation: Pin or otherwise verify the npm package in sensitive environments before installing or running the CLI.

## Reference(s):

- [Clawdhub 1.0.0 skill page](https://clawhub.ai/djmarkd38/skills/clawdhub-1-0-0)
- [djmarkd38 publisher profile](https://clawhub.ai/user/djmarkd38)
- [ClawdHub registry](https://clawdhub.com)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes npm installation, authentication, search, install, update, list, publish, registry, and working-directory guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
