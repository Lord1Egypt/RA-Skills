## Description:

Guides agents through cloning and synchronizing GitHub repositories with Git, including SSH or HTTPS authentication, branch and submodule options, shallow clones, updates, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duanc-chao](https://clawhub.ai/user/duanc-chao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to have an agent choose and explain GitHub clone and sync workflows for public or private repositories based on authentication, branch, submodule, and network needs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Git clone and sync commands can create, update, or replace local repository directories.

Mitigation: Confirm repository URLs and target paths before execution, and require explicit approval before deleting folders or replacing existing directories.

Risk: Authentication guidance can expose private keys, tokens, or credentials if handled carelessly.

Mitigation: Use trusted repository URLs, rely on SSH agents or credential managers, and avoid sharing private keys or tokens in prompts, logs, or command history.

Risk: Global Git proxy or certificate settings can weaken network security or affect unrelated repositories.

Mitigation: Avoid changing global proxy or certificate verification settings unless required and approved; prefer scoped repository configuration when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duanc-chao/skills/clone)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands should be adapted to the repository URL, branch, authentication method, and local path.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
