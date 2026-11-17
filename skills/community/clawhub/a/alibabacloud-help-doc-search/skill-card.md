## Description:

Searches Alibaba Cloud help documentation across the Chinese and international portals and verifies OpenAPI contract details against api.aliyun.com metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to retrieve official Alibaba Cloud documentation, read known help documents, browse product catalogs, and verify API parameters, error codes, RAM permission points, quotas, billing rules, and troubleshooting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The document-read command is under-scoped and can fetch non-Alibaba URLs or local files.

Mitigation: Avoid untrusted URLs and use explicit official Alibaba Cloud HTTPS document URLs until host, scheme, private-address, file URL, and redirect validation are enforced.

## Reference(s):

- [API Metadata](references/api-metadata.md)
- [Query Construction](references/query-construction.md)
- [Search Backend](references/search-backend.md)
- [Product Codes](references/product-codes.md)
- [RAM Policies](references/ram-policies.md)
- [ECS Scenario Guide](references/ecs-scenario-guide.md)
- [ECS Knowledge FAQ](references/ecs-knowledge-faq.md)
- [Alibaba Cloud OpenAPI Metadata](https://api.aliyun.com/meta/v1)
- [Alibaba Cloud China Help Portal](https://help.aliyun.com)
- [Alibaba Cloud International Help Portal](https://www.alibabacloud.com/help)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON results with source URLs, plus shell command examples when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only documentation and metadata lookups may include warnings or informational traces when a search path degrades.]

## Skill Version(s):

0.0.3 (source: server release evidence and references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
