## Description:

Helps users inspect, create, update, delete, generate, and optimize Alibaba Cloud Simple Log Service Logstore index configurations using the Aliyun CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to manage SLS Logstore indexes, generate configurations from structured log samples, and tune indexes for queries, write throughput, and storage cost.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Updating an index replaces its entire configuration, and deletion can interrupt indexed search and SQL analytics.

Mitigation: Back up and review the complete proposed configuration, preserve discovered fields, and confirm changes before applying or deleting.

Risk: Overbroad cloud permissions or exposed access keys could allow unintended index changes.

Mitigation: Use a RAM profile scoped to the intended project and Logstore; configure credentials outside the chat and never paste access keys.

Risk: Installing an unverified vendor CLI download with elevated privileges could compromise the host.

Mitigation: Verify vendor CLI downloads before running installation commands with sudo.

## Reference(s):

- [Manage index configuration](references/manage-index-config.md)
- [Generate index configuration from logs](references/generate-index-from-logs.md)
- [Optimize index configuration](references/optimize-index-config.md)
- [RAM policies](references/ram-policies.md)
- [Alibaba Cloud SLS index APIs](references/related-apis.md)
- [Alibaba Cloud UpdateIndex API](https://help.aliyun.com/zh/sls/developer-reference/api-sls-2020-12-30-updateindex)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with JSON configuration and CLI command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline generation from supplied samples is possible; applying changes requires an authorized Alibaba Cloud profile.]

## Skill Version(s):

0.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
