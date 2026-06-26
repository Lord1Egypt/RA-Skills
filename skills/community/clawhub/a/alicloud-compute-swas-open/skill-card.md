## Description: <br>
Manage Alibaba Cloud Simple Application Server resources through SWAS OpenAPI workflows for instance inventory, lifecycle operations, command execution, firewall rules, storage, images, tags, monitoring, and lightweight database tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect and administer Alibaba Cloud Simple Application Server resources with bounded, region-aware workflows. It is suited for inventory, status summaries, controlled lifecycle changes, Cloud Assistant command execution, and SSH access repair when credentials and target resources are explicitly provided. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer real Alibaba Cloud SWAS resources using the user's credentials. <br>
Mitigation: Use a least-privilege RAM role or short-lived credentials, require explicit confirmation for every mutating operation, and verify target region and resource identifiers before execution. <br>
Risk: The SSH repair helper can persistently enable privileged SSH access on a cloud instance. <br>
Mitigation: Review scripts/fix_ssh_access.py before use and confirm the target instance, target user, public-key fingerprint, SSH port, and whether root SSH login should be enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cinience/alicloud-compute-swas-open) <br>
- [Publisher profile](https://clawhub.ai/user/cinience) <br>
- [API overview](references/api_overview.md) <br>
- [Endpoints](references/endpoints.md) <br>
- [Command Assistant](references/command-assistant.md) <br>
- [Official source list](references/sources.md) <br>
- [Alibaba Cloud SWAS OpenAPI overview](https://help.aliyun.com/zh/simple-application-server/developer-reference/api-swas-open-2020-06-01-overview) <br>
- [Alibaba Cloud SWAS InvokeCommand API](https://help.aliyun.com/zh/simple-application-server/developer-reference/api-swas-open-2020-06-01-invokecommand) <br>
- [Alibaba Cloud SWAS service endpoints](https://help.aliyun.com/zh/simple-application-server/developer-reference/service-endpoints) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell and Python examples, plus optional TSV or JSON command output from bundled helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write operational evidence and API response summaries under output/alicloud-compute-swas-open/ when the user asks to save results.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact SKILL.md frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
