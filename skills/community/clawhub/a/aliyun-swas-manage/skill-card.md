## Description: <br>
Use when managing Alibaba Cloud Simple Application Server (SWAS OpenAPI 2020-06-01) resources end-to-end, including querying instances, starting/stopping/rebooting, executing commands (cloud assistant), managing disks/snapshots/images, firewall rules/templates, key pairs, tags, monitoring, and lightweight database operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to administer Alibaba Cloud Simple Application Server resources, inspect inventory and status, run Cloud Assistant commands, and manage related disks, snapshots, images, firewall rules, key pairs, tags, monitoring, and lightweight database operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Alibaba Cloud SWAS resources and perform high-impact cloud changes. <br>
Mitigation: Use least-privilege or temporary Alibaba Cloud credentials, run a minimal read-only query first, and require explicit approval before mutating actions. <br>
Risk: Cloud Assistant command execution can run scripts on target instances. <br>
Mitigation: Confirm region, instance IDs, operating system, command type, timeout, and expected scope before execution, then verify results with query APIs. <br>
Risk: fix_ssh_access.py can create long-lived SSH access and weaken root-login policy on a target instance. <br>
Mitigation: Treat SSH repair as sensitive, review the generated access change before use, prefer temporary credentials, and avoid enabling root login unless explicitly required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-swas-manage) <br>
- [API overview and operation groups](references/api_overview.md) <br>
- [Endpoints and integration](references/endpoints.md) <br>
- [Cloud Assistant highlights](references/command-assistant.md) <br>
- [Official source list](references/sources.md) <br>
- [Alibaba Cloud SWAS OpenAPI overview](https://help.aliyun.com/zh/simple-application-server/developer-reference/api-swas-open-2020-06-01-overview) <br>
- [Alibaba Cloud SWAS InvokeCommand API](https://help.aliyun.com/zh/simple-application-server/developer-reference/api-swas-open-2020-06-01-invokecommand) <br>
- [Alibaba Cloud SWAS service endpoints](https://help.aliyun.com/zh/simple-application-server/developer-reference/service-endpoints) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; bundled scripts can emit TSV or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write command outputs, API response summaries, and evidence files under output/aliyun-swas-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
