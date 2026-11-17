## Description:

Generates read-only Jiushi Sports app order statistics by date range, keyword, and day, hour, or month grouping, including users, order counts, payment amount, refund amount, and net sales amount.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaggerliu](https://clawhub.ai/user/jaggerliu)

### License/Terms of Use:


## Use Case:

Data analysts and operations teams use this skill to query Jiushi Sports app orders for a confirmed time range, keyword filter, and hourly, daily, or monthly time bucket. The agent returns a Markdown table and concise Chinese summary of order volume, users, payments, refunds, and net sales.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided date or keyword values can affect SQL construction.

Mitigation: Use a least-privileged read-only database account, restrict access to the required table or views, and add parameterized SQL with strict date and keyword validation before deployment.

Risk: The documented query outputs do not match the executable query.

Mitigation: Align the fixed SQL template, executable query, and rendered result columns during review so users receive consistent metrics.

Risk: Runtime dependencies are not pinned.

Mitigation: Pin mysql-connector-python, pandas, and tabulate versions and scan the resolved environment before installing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jaggerliu/skills/app-order-date-key-stats)
- [Publisher Profile](https://clawhub.ai/user/jaggerliu)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown table with a Chinese summary and Python/SQL execution guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python plus mysql-connector-python, pandas, and tabulate; database credentials are read from environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter says 1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
