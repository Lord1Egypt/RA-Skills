## Description:

Use when managing Alibaba Cloud CDN via OpenAPI/SDK, including CDN domain onboarding and lifecycle operations, cache refresh/preload, HTTPS certificate updates, and log/monitoring data queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to manage Alibaba Cloud CDN domains, cache operations, HTTPS certificate settings, and monitoring or log queries while recording execution evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Alibaba Cloud credentials could allow unintended CDN domain changes or access to operational data.

Mitigation: Use least-privilege temporary Alibaba Cloud RAM credentials and confirm the exact CDN domains and region before use.

Risk: Mutating CDN APIs can delete domains, change certificates, or trigger cache refresh and preload operations.

Mitigation: Require explicit approval for domain deletion, certificate changes, cache operations, and other mutating API calls; query current state with read-only APIs first.

Risk: The metadata helper contacts official Alibaba Cloud API metadata endpoints and writes local evidence files.

Mitigation: Expect outbound access to official Alibaba Cloud endpoints and review generated evidence under output/aliyun-cdn-manage/.

## Reference(s):

- [CDN Official Sources](references/sources.md)
- [Alibaba Cloud CDN API overview (2018-05-10)](https://www.alibabacloud.com/help/en/cdn/developer-reference/api-cdn-2018-05-10-overview)
- [Alibaba Cloud CDN product page in API Explorer](https://api.aliyun.com/product/cdn)
- [Alibaba Cloud CDN OpenAPI metadata](https://api.aliyun.com/meta/v1/products/cdn/versions/2018-05-10/api-docs.json)
- [RefreshObjectCaches API reference](https://www.alibabacloud.com/help/en/cdn/developer-reference/api-cdn-2018-05-10-refreshobjectcaches)
- [SetDomainServerCertificate API reference](https://www.alibabacloud.com/help/en/cdn/developer-reference/api-cdn-2018-05-10-setdomainservercertificate)
- [DescribeDomainRealTimeRequestStatData API reference](https://www.alibabacloud.com/help/en/cdn/developer-reference/api-cdn-2018-05-10-describedomainrealtimerequeststatdata)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown with inline bash code blocks and generated JSON or Markdown evidence files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated artifacts and execution evidence are expected under output/aliyun-cdn-manage/.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
