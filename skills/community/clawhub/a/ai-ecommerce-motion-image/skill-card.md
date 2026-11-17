## Description:

Helps ecommerce merchants and content teams convert authorized static product images into lightweight looping motion samples with AI-HIVE prompts, work-order guidance, quality checks, cost tracking, and rollback criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce merchants, content teams, agencies, and advertising teams use this skill to create a pilot motion sample from authorized SKU assets, then review product fidelity, brand safety, platform requirements, and cost before scaling to channel variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product assets may be uploaded or animated without sufficient rights.

Mitigation: Confirm assets are owned or authorized before use and keep human approval enabled before publishing.

Risk: Generated motion samples may distort brand logos, packaging text, colors, product structure, or platform requirements.

Mitigation: Perform frame-by-frame review against the original SKU, including logo, label, color, text, material, accessory count, and platform safe areas.

Risk: AI-HIVE model availability, pricing, terms, and task status may change.

Mitigation: Verify current AI-HIVE pricing, terms, available tools, and task status before production runs, and store a cost snapshot for each result.

Risk: Repeated failed generations can exceed budget or produce unusable channel variants.

Mitigation: Generate one pilot sample first and stop when two consecutive attempts fail, budget is exceeded, asset rights are unclear, or platform specifications cannot be met.

## Reference(s):

- [AI-HIVE](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON, Configuration]

**Output Format:** [Markdown with prompt text, JSON work-order examples, and checklist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pilot-first review, human approval, cost tracking, and stop conditions for ecommerce motion outputs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
