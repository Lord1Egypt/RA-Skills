## Description:

CMG cloud migration support for resource scanning, Tencent Cloud product recommendations, TCO analysis, and migration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[llm-pm](https://clawhub.ai/user/llm-pm)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud migration engineers and solution architects use this skill to inventory source cloud resources, map them to Tencent Cloud offerings, obtain real pricing data, compare migration TCO, and identify the appropriate migration tool path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use powerful cloud credentials with downloaded scanner binaries and generated migration reports.

Mitigation: Install only when the publisher and scanner source are trusted; use isolated, least-privilege, preferably short-lived cloud credentials and treat generated JSON, Excel, and HTML reports as sensitive.

Risk: Recommendation requests can send cloud resource inventory and topology details to a user-supplied MCP server.

Mitigation: Use only an explicitly provided trusted HTTPS MCP endpoint, avoid fallback endpoints, and review what inventory data will be transmitted before sending it.

Risk: Scanner binaries are precompiled downloads whose artifact checksums are maintained in the skill, while upstream signatures or official checksum manifests are not evidenced.

Mitigation: Download scanners through the provided checksum flow, stop on checksum mismatch, and consider reviewing or sandboxing binaries before execution.

Risk: TCO outputs can be misleading if prices are estimated or stale.

Mitigation: Use only real API pricing or official cloud price calculators, include a price source for each item, and fail closed when current pricing cannot be retrieved.

## Reference(s):

- [CMG resource scanning guide](references/scan.md)
- [CMG recommendation guide](references/recommend.md)
- [CMG TCO analysis guide](references/tco.md)
- [CMG migration guide](references/migrate.md)
- [Cloud product code reference](references/products.md)
- [Scanner package checksums](references/CHECKSUMS.md)
- [Scanner package distribution](https://msp-release-1258344699.cos.ap-shanghai.myqcloud.com/package/urp/)
- [Tencent Cloud price calculator](https://buy.cloud.tencent.com/price)
- [Alibaba Cloud pricing](https://www.aliyun.com/price/product)
- [AWS Pricing Calculator](https://calculator.aws/#/addService)
- [Huawei Cloud pricing calculator](https://www.huaweicloud.com/pricing/calculator.html)
- [Google Cloud pricing calculator](https://cloud.google.com/products/calculator?hl=zh-CN)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, Excel, HTML, and shell-command artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scanner Excel workbooks, recommendation JSON, pricing JSON, and TCO reports.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
