## Description:

Enforce contextual permission boundaries for AI agents based on communication surface by constraining agent capabilities such as shell execution, file I/O, secrets access, messaging, and sub-agent use by channel trust level.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adroidian](https://clawhub.ai/user/adroidian)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure and audit channel-based trust tiers for AI agents operating across direct messages, private groups, and public communication surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be mistaken for a real security boundary even though the provided controls are advisory and configuration-based.

Mitigation: Use separate authenticated identity checks and runtime enforcement before allowing shell commands, file access, secrets, messaging, financial actions, or sub-agent use.

Risk: Incorrect channel defaults or trust-tier mappings can grant more capability than intended.

Mitigation: Review the configuration before deployment and run the included validator and audit scripts against the final channel mapping.

## Reference(s):

- [Permission Matrix](references/permission-matrix.md)
- [Example Configuration](references/example-config.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML configuration examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes advisory trust-tier guidance and optional local validation, audit, and channel-resolution script outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
