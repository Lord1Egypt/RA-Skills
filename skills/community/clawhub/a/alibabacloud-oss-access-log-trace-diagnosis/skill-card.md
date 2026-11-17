## Description:

Diagnoses Alibaba Cloud OSS request failures and traces object access using the customer's own logs and configuration without changing cloud resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and support engineers use this skill to investigate OSS access errors, identify applicable authorization rules, and trace object access or deletion. When evidence is unavailable, it provides qualified findings, console queries, or escalation guidance rather than claiming a confirmed cause.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to OSS configuration, access logs, and optional RAM policies may expose sensitive customer data.

Mitigation: Use a scoped, short-lived read-only role limited to the target bucket and log project.

Risk: Generated reports may expose request IDs, IP addresses, object keys, account IDs, or AccessKey IDs.

Mitigation: Treat reports as sensitive and restrict their storage and sharing.

Risk: Using diagnostic guidance as an incident-mitigation action could change resource access unexpectedly.

Mitigation: Keep this skill read-only; have the customer separately review and perform any access-control changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-access-log-trace-diagnosis)
- [Realtime access-log source](artifact/references/module1_log_source.md)
- [Error codes and verdict classes](artifact/references/module3_error_codes.md)
- [Read-only RAM permissions](artifact/references/ram-policies.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown or JSON report with findings and suggested console queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local reports may contain request identifiers, IP addresses, object keys, account IDs, and AccessKey IDs.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
