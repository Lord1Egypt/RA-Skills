## Description:

Manage Alibaba Cloud Simple Application Server (SWAS OpenAPI 2020-06-01) resources end-to-end for querying instances, starting, stopping, rebooting, executing commands, and managing disks, snapshots, images, firewall rules, key pairs, tags, monitoring, and lightweight database operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to administer Alibaba Cloud SWAS resources, inventory instances, run Cloud Assistant commands, and manage related server assets with region-aware workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SSH repair workflow can persistently grant root SSH access and change SSH policy on a target instance.

Mitigation: Use it only as break-glass tooling after reviewing the target instance, account, key fingerprint, and SSH policy; avoid root where possible.

Risk: Untrusted user, port, or public-key input can make the SSH repair workflow unsafe.

Mitigation: Provide only trusted --user, --port, and --pubkey values, and restrict Alibaba Cloud credentials to the specific resources involved.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/cinience/skills/alicloud-compute-swas-open)
- [SWAS OpenAPI overview](https://help.aliyun.com/zh/simple-application-server/developer-reference/api-swas-open-2020-06-01-overview)
- [SWAS service endpoints](https://help.aliyun.com/zh/simple-application-server/developer-reference/service-endpoints)
- [SWAS InvokeCommand reference](https://help.aliyun.com/zh/simple-application-server/developer-reference/api-swas-open-2020-06-01-invokecommand)
- [Artifact API overview](references/api_overview.md)
- [Artifact command assistant notes](references/command-assistant.md)
- [Artifact endpoints notes](references/endpoints.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, and optional TSV or JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local evidence files under output/alicloud-compute-swas-open when the workflow saves command outputs or API response summaries.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
