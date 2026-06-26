## Description: <br>
Use when managing Alibaba Cloud ESA: deploy HTML/static sites via Pages, manage Edge Routines, use Edge KV, handle site management, DNS records, cache rules, and query traffic analytics via OpenAPI/SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to administer Alibaba Cloud ESA resources, including edge site deployment, serverless edge functions, distributed key-value storage, DNS and cache configuration, and traffic analytics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to publish, modify, or delete live Alibaba Cloud ESA resources. <br>
Mitigation: Use a dedicated least-privilege RAM role and require explicit confirmation before production deployments, deletes, or configuration changes. <br>
Risk: Incorrect target identifiers could affect the wrong site, routine, domain, namespace, or DNS record. <br>
Mitigation: Review target site, routine, domain, namespace, and record IDs before executing cloud operations. <br>
Risk: Analytics exports and inventory outputs can contain sensitive operational information. <br>
Mitigation: Treat generated analytics and inventory files as sensitive and restrict where they are written or shared. <br>
Risk: Unpinned cloud SDK dependencies may change behavior over time. <br>
Mitigation: Pin Alibaba Cloud SDK versions in environments that use this skill for repeatable operations. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cinience/aliyun-esa-manage) <br>
- [Alibaba Cloud ESA API metadata](https://api.aliyun.com/meta/v1/products/ESA/versions/2024-09-10/api-docs.json) <br>
- [Alibaba Cloud ESA endpoints](https://www.alibabacloud.com/help/en/esa/developer-reference/endpoints) <br>
- [Pages Deployment Reference](references/pages.md) <br>
- [Edge Routine Reference](references/er.md) <br>
- [Edge KV Storage Reference](references/kv.md) <br>
- [ESA OpenAPI Overview](references/api_overview.md) <br>
- [DNS Records Reference](references/dns-records.md) <br>
- [Cache Reference](references/cache.md) <br>
- [Rule Expression Generation Guide](references/rule-generation-guide.md) <br>
- [Time-Series Data API](references/time-series.md) <br>
- [Top-N Data API](references/top-data.md) <br>
- [Metrics and Dimensions Reference](references/fields.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose Alibaba Cloud OpenAPI or Python SDK operations and may generate inventory or analytics output files when the user requests them.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
