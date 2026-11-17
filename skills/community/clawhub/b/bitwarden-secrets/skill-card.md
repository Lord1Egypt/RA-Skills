## Description:

Safely access Bitwarden or Vaultwarden secrets via the bw CLI with redacted outputs by default.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawbow](https://clawhub.ai/user/clawbow)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to interact with Bitwarden or Vaultwarden through the bw CLI for vault sync, item search, metadata retrieval, and tightly gated single-field reveal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bootstrap and export flow can place vault credentials into shell environment variables or plaintext export files.

Mitigation: Review and harden the bootstrap/export flow before installation; avoid writing or sourcing plaintext credential export files and prefer direct bw CLI use or redacted vw_cli.py commands until that behavior is removed or tightly gated.

Risk: Running setup from root can broaden exposure of BW_SESSION and exported credential variables.

Mitigation: Avoid running the setup from root unless strictly necessary and limit shell/session scope for any exported credentials.

Risk: Reveal mode can disclose a single secret field when enabled.

Mitigation: Use reveal only with explicit user consent, require both VW_REVEAL_ALLOW=1 and --confirm YES_REVEAL, and retrieve only the minimum needed field.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clawbow/skills/bitwarden-secrets)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default command outputs are intended to be redacted or metadata-only; revealing a secret field requires explicit consent controls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
