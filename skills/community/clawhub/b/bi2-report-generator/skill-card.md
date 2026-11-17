## Description:

Generates a BI2 business analysis report from PPTX screenshot data and saves it as an HTML report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard052317](https://clawhub.ai/user/richard052317)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and agents use this skill to turn BI2 operating metrics from PPTX screenshots into a multi-section HTML operating analysis report covering revenue, margin, expenses, customers, products, inventory, receivables, forecasts, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary says the skill embeds Feishu app credentials.

Mitigation: Remove the embedded secret, rotate the exposed credential, and require runtime secret injection from a managed secret store.

Risk: The security summary says sensitive business reports can be sent externally without clear per-run user control.

Mitigation: Make Feishu sending explicit and opt-in for each run, and confirm the recipient before upload or message delivery.

Risk: The security guidance calls out recipient and output-path uncertainty, including unknown users.

Mitigation: Confirm the output path and recipient, and fail closed for unmapped users instead of falling back to a default recipient or folder.

Risk: The security guidance calls out an unpinned remote Chart.js dependency.

Mitigation: Remove the remote dependency or pin it with integrity controls before using the generated report with sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richard052317/skills/bi2-report-generator)
- [Publisher profile](https://clawhub.ai/user/richard052317)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [HTML report file with concise agent status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report is saved to a mapped local user folder and may be sent through Feishu when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
