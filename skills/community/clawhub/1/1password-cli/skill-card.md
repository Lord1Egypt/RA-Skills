## Description:

Securely access and manage secrets with the 1Password CLI using a service account token for vault operations such as reading, writing, editing, and deleting items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sichengchen](https://clawhub.ai/user/sichengchen)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure 1Password CLI access for agents and perform controlled secret-management tasks in a dedicated vault.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad secret read, write, edit, and delete workflows through the 1Password CLI.

Mitigation: Limit the 1Password service account to a dedicated vault and require explicit approval before create, edit, or delete actions.

Risk: Secrets or service account tokens could be exposed through command arguments, logs, console output, or persistent caches.

Mitigation: Avoid placing real secrets directly in shell commands, do not print tokens or retrieved secrets unless explicitly approved, and prohibit persistent caching unless it is encrypted, short-lived, and access-controlled.

## Reference(s):

- [1Password CLI get started documentation](https://developer.1password.com/docs/cli/get-started)
- [1Password Developer Portal](https://developer.1password.com/)
- [ClawHub skill page](https://clawhub.ai/sichengchen/skills/1password-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup steps, operational command examples, troubleshooting notes, and safety practices for handling 1Password service account tokens and retrieved secrets.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
