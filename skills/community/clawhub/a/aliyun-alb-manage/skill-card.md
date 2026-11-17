## Description:

Helps agents inspect, create, change, and troubleshoot Alibaba Cloud Application Load Balancer resources, including ALB instances, listeners, server groups, rules, certificates, ACLs, security policies, and health checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inventory, diagnose, and perform controlled changes for Alibaba Cloud ALB resources. It supports read-only inspection, lifecycle operations, health validation, and troubleshooting workflows with saved command outputs and before/after evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make production-affecting Alibaba Cloud ALB changes, including create, update, stop, remove, and delete operations.

Mitigation: Use restricted IAM or short-lived STS credentials, run read-only inventory first, and require explicit approval before executing change commands.

Risk: Some destructive operations provide a --yes option that can bypass confirmation prompts.

Mitigation: Avoid --yes in automation and require a human-reviewed change window for lifecycle operations.

Risk: Saved outputs may contain infrastructure, traffic, listener, backend, certificate, ACL, or health-check details.

Mitigation: Protect output/aliyun-alb-manage/ files with appropriate access controls and clean them up when no longer needed.

## Reference(s):

- [ALB API Quick Map](references/api_quick_map.md)
- [ALB Scripts Catalog](references/scripts_catalog.md)
- [ALB Troubleshooting Guide](references/troubleshooting.md)
- [ALB Access Log Analysis](references/log-analysis.md)
- [ALB Resource Dependencies and Creation Order](references/resource-dependencies.md)
- [ALB Official Sources](references/sources.md)
- [Alibaba Cloud ALB API Overview](https://api.aliyun.com/document/Alb/2020-06-16/overview)
- [Alibaba Cloud ALB API Explorer Product Page](https://api.aliyun.com/product/Alb)
- [Alibaba Cloud ALB OpenAPI Metadata](https://api.aliyun.com/meta/v1/products/Alb/versions/2020-06-16/api-docs.json)
- [Alibaba Cloud API Explorer](https://api.aliyun.com/)
- [Alibaba Cloud ALB FAQ](https://help.aliyun.com/zh/slb/application-load-balancer/support/faq-about-alb)
- [Alibaba Cloud ALB Status Code Reference](https://help.aliyun.com/zh/slb/application-load-balancer/support/alb-exception-status-code-description)
- [Alibaba Cloud ALB Health Check Troubleshooting](https://help.aliyun.com/zh/slb/application-load-balancer/support/how-do-i-troubleshoot-health-check-errors)
- [Alibaba Cloud ALB Access Logs](https://help.aliyun.com/zh/slb/application-load-balancer/user-guide/access-logs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON or text command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Command outputs, request parameters, API responses, and before/after snapshots may be saved under output/aliyun-alb-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
