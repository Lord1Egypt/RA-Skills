## Description: <br>
Use when managing Alibaba Cloud CDN via OpenAPI/SDK, including CDN domain onboarding and lifecycle operations, cache refresh/preload, HTTPS certificate updates, and log/monitoring data queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and execute Alibaba Cloud CDN domain lifecycle work, cache refresh or preload operations, HTTPS certificate updates, and CDN log or monitoring queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alibaba Cloud credentials could authorize changes beyond the intended CDN task. <br>
Mitigation: Use temporary least-privilege RAM or STS credentials and verify the active account before running the skill. <br>
Risk: CDN-changing operations could affect live domains, cache state, or certificate configuration. <br>
Mitigation: Require explicit approval for mutating operations and query current state with read-only APIs before making changes. <br>
Risk: Generated evidence files may expose infrastructure details. <br>
Mitigation: Review files under output/aliyun-cdn-manage/ before sharing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-cdn-manage) <br>
- [CDN Official Sources](references/sources.md) <br>
- [Alibaba Cloud CDN API overview](https://www.alibabacloud.com/help/en/cdn/developer-reference/api-cdn-2018-05-10-overview) <br>
- [Alibaba Cloud CDN API Explorer](https://api.aliyun.com/product/cdn) <br>
- [CDN OpenAPI metadata](https://api.aliyun.com/meta/v1/products/cdn/versions/2018-05-10/api-docs.json) <br>
- [RefreshObjectCaches API](https://www.alibabacloud.com/help/en/cdn/developer-reference/api-cdn-2018-05-10-refreshobjectcaches) <br>
- [SetDomainServerCertificate API](https://www.alibabacloud.com/help/en/cdn/developer-reference/api-cdn-2018-05-10-setdomainservercertificate) <br>
- [DescribeDomainRealTimeRequestStatData API](https://www.alibabacloud.com/help/en/cdn/developer-reference/api-cdn-2018-05-10-describedomainrealtimerequeststatdata) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands plus generated JSON and Markdown evidence files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated artifacts and API response summaries are expected under output/aliyun-cdn-manage/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
