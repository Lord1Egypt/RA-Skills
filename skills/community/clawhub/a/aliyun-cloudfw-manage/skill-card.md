## Description: <br>
Use when managing Alibaba Cloud Cloud Firewall (Cloudfw) via OpenAPI/SDK, including the user requests firewall policy/resource operations, change management, status checks, or troubleshooting Cloud Firewall API workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud security engineers use this skill to discover Alibaba Cloud Cloud Firewall APIs, prepare and review firewall policy/resource operations, check status, and troubleshoot Cloud Firewall API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Firewall policy or resource changes can affect cloud network security posture. <br>
Mitigation: Use least-privilege Alibaba Cloud credentials and require user confirmation of the exact region, resource identifier, and action before any mutating API call. <br>
Risk: Saved API output may reveal firewall configuration or operational details. <br>
Mitigation: Keep generated artifacts under output/aliyun-cloudfw-manage/ private and avoid sharing response payloads unless they have been reviewed for sensitive information. <br>
Risk: Ambiguous region selection can target the wrong Alibaba Cloud environment. <br>
Mitigation: Use ALICLOUD_REGION_ID when available and ask the user to choose a region before running mutating operations when the region is unclear. <br>


## Reference(s): <br>
- [Aliyun Cloudfw Manage on ClawHub](https://clawhub.ai/cinience/aliyun-cloudfw-manage) <br>
- [Sources](references/sources.md) <br>
- [Alibaba Cloud Cloudfw OpenAPI Product Page](https://api.aliyun.com/product/Cloudfw) <br>
- [Cloudfw API Metadata](https://api.aliyun.com/meta/v1/products/Cloudfw/versions/2017-12-07/api-docs.json) <br>
- [Cloudfw Single API Definition](https://api.aliyun.com/meta/v1/products/Cloudfw/versions/2017-12-07/apis/{ApiName}/api.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration, Files, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and saved JSON or Markdown API inventory artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saved artifacts should be written under output/aliyun-cloudfw-manage/ with key region, resource, action, and time-range parameters captured for reproducibility.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
