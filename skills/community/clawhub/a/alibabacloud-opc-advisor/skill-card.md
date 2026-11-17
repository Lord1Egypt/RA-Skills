## Description:

Advises non-technical solo founders, in Chinese, on Alibaba Cloud OPC package selection, pricing, purchase links, and launch or migration paths without deploying resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to guide Chinese-speaking one-person-company founders through Alibaba Cloud OPC SKU selection for first launches or migrations. It asks for scale and user-data signals, recommends one standard package, explains assumptions and upgrade triggers, and points to purchase or deployment handoff paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advisor may make package recommendations for paid Alibaba Cloud resources feel like approval to create or order those resources.

Mitigation: Use it as read-only selection guidance only; require a separate deployment or checkout flow with explicit price, resource, recurring-billing, DNS, and account-ownership confirmation before any paid action.

## Reference(s):

- [Alibaba Cloud OPC Advisor](SKILL.md)
- [A1 Zero-Start Output Template](references/a1-zero-start.md)
- [A2 Migration Output Template](references/a2-migration.md)
- [SKU Sizing Questionnaire](references/sku-sizing-questionnaire.md)
- [OPC SKU Matrix](references/skus.md)
- [Concurrent Users Triage & SKU Mapping Guide](references/concurrency-to-sku.md)
- [OPC Cloud Advisor Self-Check Checklists](references/checklists.md)
- [UGC Application Hardening Checklist](references/ugc-application-hardening.md)
- [Purchase / Console Entry-Point Canonical Registry](references/purchase-url-canonical.md)
- [OPC Package Page](https://opc.aliyun.com/products)
- [Alibaba Cloud Domain Registration](https://wanwang.aliyun.com/)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Chinese conversational Markdown with a structured recommendation and plain-language next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only advisor output; no files, shell commands, or resource deployment are produced by this skill.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
