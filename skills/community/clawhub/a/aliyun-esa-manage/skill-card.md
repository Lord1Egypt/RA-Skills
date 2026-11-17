## Description:

Guides agents in managing Alibaba Cloud ESA resources, including Pages deployments, Edge Routines, Edge KV, site and DNS configuration, cache rules, and traffic analytics through Alibaba Cloud OpenAPI and the official Python SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to plan and execute Alibaba Cloud ESA administration tasks such as deploying edge pages, managing Edge Routine functions and KV storage, configuring sites, DNS, and cache behavior, and querying analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can publish deployments to production ESA environments.

Mitigation: Review intended targets before execution, prefer read-only checks first, and avoid production deployment defaults unless explicitly approved.

Risk: Static deployment flows can expose local files if deployment directories include secrets or symlinks.

Mitigation: Inspect deployment directories before packaging and exclude credentials, generated secrets, symlinks, and unrelated local files.

Risk: Analytics exports may contain sensitive traffic or request data.

Mitigation: Write exports only to approved locations, restrict permissions, and clean up files when they are no longer needed.

Risk: Alibaba Cloud credentials may authorize broad changes to ESA resources.

Mitigation: Use least-privilege RAM credentials and prefer scoped or read-only permissions for inventory and analytics tasks.

## Reference(s):

- [ESA OpenAPI Overview](references/api_overview.md)
- [ESA Pages Deployment Reference](references/pages.md)
- [Edge Routine Reference](references/er.md)
- [Edge KV Storage Reference](references/kv.md)
- [ESA Sites](references/sites.md)
- [ESA DNS Records](references/dns-records.md)
- [ESA Cache](references/cache.md)
- [DescribeSiteTimeSeriesData API Reference](references/time-series.md)
- [DescribeSiteTopData API Reference](references/top-data.md)
- [Metrics and Dimensions Reference](references/fields.md)
- [ESA Rule Expression Generation Guide](references/rule-generation-guide.md)
- [ESA OpenAPI Metadata](https://api.aliyun.com/meta/v1/products/ESA/versions/2024-09-10/api-docs.json)
- [Alibaba Cloud ESA Endpoints](https://www.alibabacloud.com/help/en/esa/developer-reference/endpoints)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline code, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run Alibaba Cloud SDK scripts and store inventory or analytics outputs under output/aliyun-esa-manage/.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
