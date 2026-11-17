## Description:

Governance: immutable, timestamped, hash-chained audit log of all agent actions for compliance, investigation, and accountability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arhadnane](https://clawhub.ai/user/arhadnane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and governance reviewers use this skill to create and inspect a tamper-evident audit trail of agent actions for investigation, compliance review, and accountability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill records broad agent activity metadata and possible tool arguments, which can include sensitive context.

Mitigation: Install only where local retention of agent activity metadata is acceptable; use workspace confinement, restrictive file permissions, retention controls, and stronger redaction before sensitive use.

Risk: Immutability and compliance-grade audit claims may exceed the guarantees of local append-only log files.

Mitigation: Treat the logs as tamper-evident local records, not as a complete compliance system; review integrity, deletion, purge, and backup controls before relying on them.

Risk: Weak redaction and path controls can expose secrets or place audit data outside the intended storage boundary.

Mitigation: Review redaction coverage, avoid use around secrets until controls are improved, and constrain writable paths to approved audit storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arhadnane/skills/audit-trail)
- [Publisher profile](https://clawhub.ai/user/arhadnane)

## Skill Output:

**Output Type(s):** [Files, JSON, Analysis, Guidance]

**Output Format:** [JSON and JSONL files with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes audit records, verification results, query matches, and compliance reports under .security/audit-trail when invoked.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, index.js)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
