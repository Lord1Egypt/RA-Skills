## Description:

Use when managing Alibaba Cloud Simple Application Server (SWAS OpenAPI 2020-06-01) resources end-to-end, including querying instances, starting, stopping, rebooting, executing Cloud Assistant commands, and managing disks, snapshots, images, firewall rules, key pairs, tags, monitoring, and lightweight database operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage Alibaba Cloud Simple Application Server resources, run inventory and summary workflows, execute Cloud Assistant commands, and verify changes with follow-up queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Alibaba Cloud administrative authority can affect production resources if credentials or regions are over-broad.

Mitigation: Use least-privilege RAM credentials, confirm region and resource identifiers before mutating operations, run an initial read-only query, and verify state after changes.

Risk: The SSH repair helper can grant persistent root SSH access and executes privileged remote commands.

Mitigation: Avoid the helper unless it has been reviewed and constrained; prefer non-root, audited, reversible recovery and do not run it with untrusted parameters or key files.

## Reference(s):

- [API overview and operation groups](references/api_overview.md)
- [Endpoints and integration](references/endpoints.md)
- [Cloud Assistant highlights](references/command-assistant.md)
- [Official source list](references/sources.md)
- [Alibaba Cloud SWAS OpenAPI overview](https://help.aliyun.com/zh/simple-application-server/developer-reference/api-swas-open-2020-06-01-overview)
- [Alibaba Cloud SWAS InvokeCommand](https://help.aliyun.com/zh/simple-application-server/developer-reference/api-swas-open-2020-06-01-invokecommand)
- [Alibaba Cloud SWAS service endpoints](https://help.aliyun.com/zh/simple-application-server/developer-reference/service-endpoints)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell commands; helper scripts may emit TSV, JSON, or command identifiers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save command outputs, API response summaries, and evidence files under output/aliyun-swas-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
