## Description:

Encrypted credential storage for OpenClaw agents. Stop storing API keys in plaintext.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Credential Vault to store, retrieve, export, rotate, and audit local API keys and tokens for OpenClaw workflows without keeping them in plaintext .env files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented eval-based environment export workflows can run unintended shell commands when used with untrusted or imported secret values.

Mitigation: Use env export only with trusted vault entries; inspect generated assignments before eval when values were imported from external sources.

Risk: Retrieved or exported secrets can be exposed through terminal output, shell history, process environments, or logs.

Mitigation: Avoid printing secrets, run commands in controlled local shells, and clear sensitive environment variables when the workflow is complete.

Risk: The unlocked session file should be treated as equivalent to access to all stored credentials.

Mitigation: Run vault lock before logout, reboot, or leaving the machine unattended, and avoid use on shared machines.

Risk: The vault is a local development convenience and is not designed for production or team-wide secret management.

Mitigation: Use a dedicated production secrets manager for servers, CI/CD, shared machines, or multi-user access.

## Reference(s):

- [Credential Vault on ClawHub](https://clawhub.ai/chloepark85/skills/credential-vault)
- [README](README.md)
- [Usage Examples](EXAMPLE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, Python snippets, and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local encrypted vault files, plaintext audit logs without secret values, and environment variable assignments when commands are run.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact pyproject.toml reports 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
