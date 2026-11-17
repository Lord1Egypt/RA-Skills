## Description:

Securely access and manage secrets using the 1Password CLI with a Service Account token for reading, writing, and editing items in a dedicated vault.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reiy-leo](https://clawhub.ai/user/reiy-leo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure agents for 1Password CLI access through a narrowly scoped service account. It supports vault and item workflows such as authentication checks, listing vaults, reading items, creating secure notes, editing fields, and deleting items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can read, create, edit, or delete secrets if the configured service account has broad vault permissions.

Mitigation: Use a narrowly scoped 1Password service account and a dedicated vault with only the permissions needed for the agent's task.

Risk: Credential values may be exposed through command-line arguments, console output, cached results, or shared agent storage.

Mitigation: Avoid putting real secrets in command-line arguments, do not print tokens or retrieved secrets unless explicitly required, and do not cache secrets in plaintext.

Risk: Create, edit, and delete commands can accidentally change or remove credentials.

Mitigation: Require explicit confirmation before mutating actions and specify the target vault to avoid ambiguous operations.

## Reference(s):

- [1Password CLI getting started](https://developer.1password.com/docs/cli/get-started)
- [1Password Developer Portal](https://developer.1password.com/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that may return JSON from the 1Password CLI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
