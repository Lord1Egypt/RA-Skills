## Description: <br>
Use when managing and troubleshoot Alibaba Cloud ALB (Application Load Balancer), including the user asks to inspect, create, change, or debug ALB instances, listeners, server groups, rules, certificates, ACLs, security policies, or health checks in Alibaba Cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and operations teams use this skill to inspect, create, update, delete, and troubleshoot Alibaba Cloud Application Load Balancer resources through guided workflows and local Python scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Lifecycle commands can stop listeners, remove backends, delete load balancers, or disable deletion protection, which can interrupt production traffic. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials, confirm the region and resource IDs, apply one change at a time, and keep before/after snapshots plus health-check results. <br>
Risk: Incorrect ALB dependency ordering can cause failed changes or leave partially configured resources. <br>
Mitigation: Follow the documented creation and deletion order, wait for asynchronous jobs when needed, and re-query final listener, server group, rule, and health state. <br>


## Reference(s): <br>
- [ALB API Quick Map](references/api_quick_map.md) <br>
- [ALB Scripts Catalog](references/scripts_catalog.md) <br>
- [ALB Troubleshooting Guide](references/troubleshooting.md) <br>
- [ALB Access Log Analysis](references/log-analysis.md) <br>
- [ALB Resource Dependencies and Creation Order](references/resource-dependencies.md) <br>
- [ALB Official Sources](references/sources.md) <br>
- [ALB API Overview](https://api.aliyun.com/document/Alb/2020-06-16/overview) <br>
- [ALB Product Page in API Explorer](https://api.aliyun.com/product/Alb) <br>
- [ALB OpenAPI Metadata](https://api.aliyun.com/meta/v1/products/Alb/versions/2020-06-16/api-docs.json) <br>
- [Alibaba Cloud API Explorer](https://api.aliyun.com/) <br>
- [Publisher Profile](https://clawhub.ai/user/cinience) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON evidence files produced by scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command outputs, request parameters, API responses, before/after snapshots, and health-check results are saved under output/aliyun-alb-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
