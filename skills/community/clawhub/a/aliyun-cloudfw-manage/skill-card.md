## Description:

Use when managing Alibaba Cloud Cloud Firewall (Cloudfw) via OpenAPI/SDK, including firewall policy and resource operations, change management, status checks, and troubleshooting Cloud Firewall API workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud security operators use this skill to manage and troubleshoot Alibaba Cloud Cloud Firewall workflows through OpenAPI or SDK-based operations. It supports metadata-first API discovery, resource and policy changes, status checks, and reproducible local output capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutating Cloud Firewall operations can change firewall policies or resources.

Mitigation: Use least-privilege Alibaba Cloud credentials and review any proposed Create, Update, Modify, or Set action before execution.

Risk: Generated API inventories or response summaries may contain operational details from the target Alibaba Cloud environment.

Mitigation: Keep generated outputs in output/aliyun-cloudfw-manage/ and avoid storing unnecessary secrets or sensitive API response content.

## Reference(s):

- [Artifact sources reference](references/sources.md)
- [Alibaba Cloud OpenAPI Cloud Firewall product page](https://api.aliyun.com/product/Cloudfw)
- [Cloudfw 2017-12-07 API metadata list](https://api.aliyun.com/meta/v1/products/Cloudfw/versions/2017-12-07/api-docs.json)
- [Cloudfw single API metadata definition](https://api.aliyun.com/meta/v1/products/Cloudfw/versions/2017-12-07/apis/{ApiName}/api.json)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-cloudfw-manage)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON or Markdown artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated API inventory and evidence outputs are expected under output/aliyun-cloudfw-manage/.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
