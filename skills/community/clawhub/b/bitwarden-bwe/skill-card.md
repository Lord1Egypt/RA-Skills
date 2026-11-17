## Description:

Manage secrets with the Bitwarden CLI by loading Secure Notes into shell sessions, creating or updating notes from environment files, listing vault items, and setting up Bitwarden CLI usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stevengonsalvez](https://clawhub.ai/user/stevengonsalvez)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to configure Bitwarden CLI workflows and request shell commands for loading, creating, listing, and managing secrets in agent or terminal sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bitwarden note contents may be evaluated as shell code when secrets are loaded into a session.

Mitigation: Use only trusted vault items, avoid shared or broadly editable notes, review note contents before loading, and prefer strict key/value parsing where possible.

Risk: Creating a note from the current shell can capture more environment variables than intended.

Mitigation: Review the active environment before using current-shell export workflows and prefer a purpose-built .env file containing only required secrets.

Risk: Secrets can persist in the shell environment after loading.

Mitigation: Load secrets only into the needed terminal session, lock Bitwarden when done, and close or clear the session after use.

## Reference(s):

- [Bitwarden CLI Documentation](https://bitwarden.com/help/cli/)
- [Bitwarden CLI Reference](references/cli-reference.md)
- [ClawHub Skill Page](https://clawhub.ai/stevengonsalvez/skills/bitwarden-bwe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Bitwarden CLI (bw) and jq; outputs may include commands that handle secrets.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
