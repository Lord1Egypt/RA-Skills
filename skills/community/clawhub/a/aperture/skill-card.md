## Description:

Install and run Aperture, the L402 Lightning reverse proxy from Lightning Labs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roasbeef](https://clawhub.ai/user/roasbeef)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install, configure, start, and stop an L402-aware reverse proxy for payment-gated API endpoints, paid content, and L402 authentication testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install flow uses a mutable upstream Aperture version.

Mitigation: Prefer a pinned Aperture version before installation.

Risk: Aperture runs with access to Lightning invoice credentials.

Mitigation: Run Aperture as an unprivileged user and keep the macaroon limited to invoice-only permissions.

Risk: Development options can disable TLS or L402 authentication.

Mitigation: Use --insecure or --no-auth only in isolated local development.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roasbeef/skills/aperture)
- [Aperture project documentation](https://github.com/lightninglabs/aperture)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scripts that can install upstream Aperture, generate local configuration, and manage a background Aperture process.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
