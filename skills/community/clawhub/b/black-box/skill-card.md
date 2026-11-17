## Description:

Indestructible audit logs for agent actions, stored in TiDB Zero.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilyjazz](https://clawhub.ai/user/lilyjazz)

### License/Terms of Use:


## Use Case:

Developers and operators use Black Box to record agent actions, errors, and command intent to a persistent TiDB-backed audit trail, then read recent records for debugging, compliance review, or incident reconstruction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends agent activity, prompts, commands, or other sensitive log content to cloud storage.

Mitigation: Use only an approved database and require explicit user or administrator opt-in before enabling cloud logging.

Risk: Database credentials and connection strings may be weakly scoped or stored with insufficient protection.

Mitigation: Store DSNs and TIDB_* credentials with owner-only permissions or a secret manager, and rotate credentials if logs or configuration are exposed.

Risk: Audit logs may capture reasoning chains, sensitive command details, customer data, or compliance evidence.

Mitigation: Avoid logging reasoning chains or sensitive command details, and define retention, access review, and redaction practices before deployment.

Risk: Networked database logging depends on external services and transport security.

Mitigation: Pin dependencies, enforce verified TLS, and validate the approved TiDB endpoint before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lilyjazz/skills/black-box)
- [TiDB Zero provisioning API endpoint](https://zero.tidbapi.com/v1alpha1/instances)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON responses and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads TiDB audit log records; requires pymysql, curl, outbound network access, and TIDB_* credentials or fallback provisioning.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
