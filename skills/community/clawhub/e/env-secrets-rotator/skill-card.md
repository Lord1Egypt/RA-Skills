## Description:

Rotate and update secrets in environment files, generate Vault commands, and manage secret rotation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to rotate values in local .env files, validate simple environment files, preview rotations, and generate HashiCorp Vault CLI commands for manual secret updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Newly generated secret values may be saved in plaintext rotation history in the user's home directory.

Mitigation: Use dry-run first, avoid real credentials until reviewed, and delete or restrict access to ~/.env-rotation-history.json after any rotation involving sensitive values.

Risk: Rotated values and generated Vault commands can expose secrets in terminal output, logs, or shared agent sessions.

Mitigation: Run in a private local session, avoid logged CI, and redact command output before sharing.

Risk: The skill edits local .env files and can create backup files containing previous secret values.

Mitigation: Review the target file path, use dry-run before modification, and secure or remove backup files after validating the rotation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/derick001/skills/env-secrets-rotator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local file updates, backup files, JSON rotation summaries, Vault CLI commands, and validation results.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
