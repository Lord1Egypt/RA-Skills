## Description:

Runs an on-demand Azure Key Vault health check through Azure Managed Grafana, summarizing fleet availability, latency, throttling, authentication failures, saturation, and targeted deep-dive findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1w2w3y](https://clawhub.ai/user/1w2w3y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to inspect Azure Key Vault health across configured Azure subscriptions, identify significant vault issues, and produce prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to Azure Managed Grafana telemetry for configured subscriptions.

Mitigation: Grant only the minimum required Azure Managed Grafana access for the intended subscriptions.

Risk: The setup flow uses a bearer token in a shell command.

Mitigation: Use a least-privilege, short-lived Grafana service-account token and avoid pasting it into shell history.

Risk: Persistent health-check reports may contain subscription IDs, vault names, caller IPs, app IDs, and secret or key object references.

Mitigation: Review or redact memory/amg-check-key-vault reports before sharing logs or workspace files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1w2w3y/skills/amg-check-key-vault)
- [Analysis patterns](artifact/reference/analysis-patterns.md)
- [Deep-dive queries](artifact/reference/deep-dive-queries.md)
- [Error handling](artifact/reference/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown operational report with inventory summaries, telemetry findings, KQL query results, and prioritized action items.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local configuration and known-issue report files for the configured health-check workspace.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
