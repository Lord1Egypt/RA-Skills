## Description:

Runs the local Cline CLI for coding, scaffolding, debugging, and multistep planning tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elathoxu-crypto](https://clawhub.ai/user/elathoxu-crypto)

### License/Terms of Use:


## Use Case:

Developers use this skill to invoke an installed local Cline CLI from an agent workflow for coding, repo scaffolding, debugging, and short task-oriented planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run broad coding tasks through auto-approved headless Cline CLI execution without strong scope controls.

Mitigation: Use it only in a limited workspace, review tasks before invocation, and pay special attention to deletions, package installs, network access, or commands outside the project.

Risk: Prompts or workspace context may expose secrets to the local CLI workflow.

Mitigation: Do not paste secrets into prompts, and keep sensitive files out of the workspace context used with this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elathoxu-crypto/skills/cline)
- [Publisher profile](https://clawhub.ai/user/elathoxu-crypto)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown or plain text with command output and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Depends on the local Cline CLI task and workspace context.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
