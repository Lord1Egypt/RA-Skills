## Description:

Query and back up Alibaba Cloud WAF 3.0 billing data, including instance information, daily bill summaries, hourly fee breakdowns, and local JSON/CSV exports via aliyun-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, cloud administrators, security engineers, and FinOps teams use this skill to inspect Alibaba Cloud WAF 3.0 billing, estimate SeCU/Credit costs, and keep local billing backups for audit or cost review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an existing Alibaba Cloud CLI profile to read WAF billing data and write local backup files.

Mitigation: Install only for this billing backup purpose, use the documented read-only RAM policy, and review the generated local backup files according to the user's data handling requirements.

Risk: Access keys or credential files could be exposed if credential setup is performed inside the agent session.

Mitigation: Configure Alibaba Cloud credentials outside the agent session, use only aliyun configure list for status checks, and avoid entering AK/SK values directly in conversation.

Risk: Pay-as-you-go WAF billing has T+1 settlement behavior, so same-day final billing requests can be misleading.

Mitigation: State when today's data is estimated and adjust final-bill queries to the prior settled day unless the user explicitly requests an estimate.

## Reference(s):

- [Aliyun CLI Installation and Configuration Guide](references/cli-installation-guide.md)
- [RAM Permission Policies](references/ram-policies.md)
- [WAF 3.0 Billing Fields and Cost Items Reference](references/billing-fields-reference.md)
- [Alibaba Cloud CLI Documentation](https://help.aliyun.com/zh/cli/)
- [Alibaba Cloud CLI Credential Configuration](https://help.aliyun.com/zh/cli/configure-credentials)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown summary with inline shell commands plus JSON and CSV backup files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates date-organized local backup files under waf-billing-backups when executed.]

## Skill Version(s):

0.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
