## Description:

Manage Alibaba Cloud Backup and Disaster Recovery Center (BDRC) via OpenAPI/SDK for backup and disaster-recovery inventory, policy and configuration changes, status checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud BDRC resources through OpenAPI or SDK workflows, including inventory, configuration changes, status checks, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud credentials could be over-privileged or exposed in logs and evidence files.

Mitigation: Use least-privilege Alibaba Cloud credentials and avoid saving secrets in command outputs, logs, or evidence artifacts.

Risk: BDRC create, update, modify, or set operations may change backup and disaster-recovery resources.

Mitigation: Confirm region, resource identifiers, and planned mutations before execution, then verify results with list or describe APIs.

Risk: Custom metadata script product or version values may affect output filenames before filename validation is added.

Mitigation: Prefer the default BDRC product/version values or use only safe product and version strings for metadata discovery.

## Reference(s):

- [Sources](references/sources.md)
- [Alibaba Cloud OpenAPI BDRC product page](https://api.aliyun.com/product/BDRC)
- [BDRC 2023-08-08 API metadata](https://api.aliyun.com/meta/v1/products/BDRC/versions/2023-08-08/api-docs.json)
- [BDRC single API metadata template](https://api.aliyun.com/meta/v1/products/BDRC/versions/2023-08-08/apis/{ApiName}/api.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration details; generated artifacts may include JSON and Markdown API inventory files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When artifacts are needed, the skill directs the agent to save command outputs and API response summaries under output/alicloud-backup-bdrc/.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
