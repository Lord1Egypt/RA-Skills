## Description:

Helps agents inspect, explain, reconcile, verify, and analyze CTYUN billing data through read-only ctyun-cli billing queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kqwjyk](https://clawhub.ai/user/kqwjyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud operators, finance analysts, and support teams use this skill to answer CTYUN billing questions, reconcile charges, and prepare concise billing reports from locally configured ctyun-cli data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may access sensitive billing, account, order, transaction, or resource identifiers while answering billing questions.

Mitigation: Use the smallest approved query scope, keep handling local, and redact identifiers in responses.

Risk: Credentials could be exposed if the agent asks for keys, runs configuration, or logs command details.

Mitigation: Require the user to configure ctyun-cli personally, never pass AccessKey or SecretKey on the command line, and do not enable logging.

Risk: Incomplete pagination, missing permissions, schema changes, or unavailable resource checks can lead to unsupported billing conclusions.

Mitigation: Disclose partial coverage, preserve bill API values as the source of truth for past charges, and report Cannot determine when needed data is missing.

## Reference(s):

- [Bill Actions and Runtime Discovery](references/bill-actions.md)
- [Billing Evidence Policy](references/evidence-policy.md)
- [Billing Privacy Policy](references/privacy-policy.md)
- [Bill Query Catalog](references/query-catalog.md)
- [Dialogue Billing Report Specification](references/report-spec.md)
- [Install ctyun-cli](references/install.md)
- [Troubleshooting Without Guessing](references/troubleshooting.md)
- [Official CTYUN ctyun-cli installation guide](https://www.ctyun.cn/document/11095072/11096343)
- [ClawHub skill page](https://clawhub.ai/kqwjyk/skills/ctyun-analyze-billing)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, analysis]

**Output Format:** [Markdown or plain text with redacted billing findings and inline ctyun-cli commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label important conclusions as Direct bill API value, Checked calculation, Partial data, or Cannot determine.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
