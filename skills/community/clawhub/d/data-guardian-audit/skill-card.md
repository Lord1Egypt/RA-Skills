## Description:

Guardian Audit records safety decisions, approvals, escalations, and execution outcomes in an append-only, hash-chained audit log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tooled-app](https://clawhub.ai/user/tooled-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and compliance reviewers use Guardian Audit to capture safety-gate decisions and review audit trails for incident analysis or compliance evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat generated reports as verified compliance proof.

Mitigation: Use reports as local audit notes unless authenticated approvals, protected append-only storage, real chain verification, restrictive file permissions, and documented event coverage are in place.

Risk: Audit logs can contain sensitive operational details, personal or business data, security decisions, and agent reasoning.

Mitigation: Restrict log access, avoid logging secrets, redact logs before sharing, configure retention, and consider encryption for shared or cloud-backed storage.

Risk: The report generator summarizes chain integrity but does not itself perform detailed verification.

Mitigation: Run the chain verification script against the audit log and correlate report outputs with the original safety-gate records before relying on them.

## Reference(s):

- [Guardian Audit Log Schema](artifact/LOG-SCHEMA.md)
- [Guardian Audit Compliance Mapping](artifact/COMPLIANCE-MAPPING.md)
- [Guardian Audit Replay and Analysis](artifact/REPLAY.md)
- [Guardian project](https://github.com/openclaw/guardian)
- [ClawHub skill page](https://clawhub.ai/tooled-app/skills/data-guardian-audit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, NDJSON audit entries, JSON status output, and optional Markdown or JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audit entries may include operational details such as file paths, commands, approval context, and agent reasoning.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
