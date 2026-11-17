## Description:

Generates order analytics for the JiuShi Sports app by product dimension, including order counts, unpaid and refunded orders, payment and refund amounts, and user counts with optional keyword and business-section filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaggerliu](https://clawhub.ai/user/jaggerliu)

### License/Terms of Use:


## Use Case:

Business analysts and operations teams use this skill to request product-level order statistics for the JiuShi Sports app over a chosen time range. It returns filtered payment, refund, order, and user metrics grouped by order title or order detail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe handling of user inputs in the live database query template.

Mitigation: Use parameterized SQL, validate time ranges, keywords, dimensions, and business-section filters, and keep the query template read-only before running against production data.

Risk: The skill can expose business order metrics and potentially sensitive small-cohort information.

Mitigation: Run only with tightly scoped read-only database credentials, restrict network access to approved environments, and apply privacy controls for small result groups.

Risk: Dependency drift could change query or rendering behavior.

Mitigation: Pin mysql-connector-python, pandas, and tabulate versions for reproducible installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jaggerliu/skills/app-order-prod-key-stats)
- [ClawHub publisher profile](https://clawhub.ai/user/jaggerliu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown tables with concise Chinese summaries and optional Python or SQL snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python plus mysql-connector-python, pandas, and tabulate; database credentials should be supplied through environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
