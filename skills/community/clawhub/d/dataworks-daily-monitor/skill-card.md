## Description:

Daily monitors Alibaba Cloud DataWorks task runs, summarizes status counts and failed tasks, and sends the report and alerts through Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexmayanjun-collab](https://clawhub.ai/user/alexmayanjun-collab)

### License/Terms of Use:

MIT-0

## Use Case:

Data platform operators and engineers use this skill to check the previous day's DataWorks task health, identify failures, and notify stakeholders through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends persistent Alibaba Cloud AccessKeys for DataWorks monitoring.

Mitigation: Use a RAM subaccount or short-lived credentials with read-only DataWorks permissions, and avoid storing AccessKeys in shell startup files or broad application configuration.

Risk: Generated Feishu reports may disclose operational task names, owners, error messages, or console links.

Mitigation: Confirm the Feishu destination before enabling notifications, and redact sensitive task details or links when they reveal business information.

## Reference(s):

- [DataWorks API Documentation](https://help.aliyun.com/document_detail/138726.html)
- [ListDagInstances API](https://help.aliyun.com/document_detail/138730.html)
- [DataWorks Monitoring Best Practices](https://help.aliyun.com/document_detail/144230.html)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown report with status counts, failed-task details, console links, and Feishu notification text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational task names, owners, error messages, and DataWorks console links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
