## Description:

Manage Alibaba Cloud databases with ApsaraDB Agent for consultation, inventory, performance diagnosis, and service-supported changes that require human confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud database operators and developers use the skill to inspect and diagnose Alibaba Cloud databases, prepare operation plans, and request supported changes through human confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an unverified downloaded installer and credential disclosure.

Mitigation: Before installation, verify that you trust the CLI distribution source and review whether the reported access-key disclosure is acceptable.

Risk: The security scan is incomplete because two files were only partially inspected.

Mitigation: Treat the scan as a review warning; the available results do not establish that all behavior is safe.

## Reference(s):

- [ApsaraDB Agent API reference](https://help.aliyun.com/zh/das/developer-reference/api-das-2020-01-16-getyaochiagent)
- [Official DAS OpenAPI catalog](https://api.aliyun.com/document/DAS)
- [CLI installation guide](artifact/references/cli-installation-guide.md)
- [RAM policies](artifact/references/ram-policies.md)
- [Operation confirmation workflow](artifact/references/operation-confirmation.md)
- [Redis memory and eviction limits](https://redis.io/faq/doc/1jbxid5qq7/is-maxmemory-the-maximum-value-of-used-memory)
- [MySQL online DDL failure conditions](https://dev.mysql.com/doc/refman/8.0/en/innodb-online-ddl-failure-conditions.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text responses and Markdown reports, including findings, inventory tables, clarification checklists, recommendations, and refusal responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operation requests may result in a service confirmation card for human review.]

## Skill Version(s):

0.2.6 (source: server-resolved release metadata and artifact/references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
