## Description:

Routes image generation and editing requests into Doubao-oriented prompt workflows for logos, IP characters, packaging, brand applications, ecommerce assets, educational visuals, media creatives, and related commercial design materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu2003li](https://clawhub.ai/user/gu2003li)

### License/Terms of Use:

MIT-0

## Use Case:

External users, designers, and marketing operators use this skill to turn creative briefs or source images into routed image-generation and image-editing work for commercial visual assets. It helps an agent select the right product reference, preserve core visual assets, and produce concise prompts or tool calls for the requested image task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: English, multilingual, legal, educational, or exact-brand-text work may be affected by the skill's strong default toward Chinese prompt conventions.

Mitigation: Tell the agent to preserve the requested language and exact visible text when those details matter.

Risk: Image outputs can contain incorrect text, invented numbers, or unsupported claims when key copy, dates, prices, discounts, credentials, or data are missing.

Mitigation: Require user-provided or confirmed values for visible text and factual claims; otherwise omit them or ask for clarification.

Risk: Brand, logo, product, character, or layout consistency can be lost if follow-up work is generated from text alone.

Mitigation: Use the confirmed core asset or source image with image-editing workflows for derivative or consistency-sensitive outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gu2003li/skills/doubao-creative-design)
- [Main skill routing rules](SKILL.md)
- [Logo system](references/brand-logo-system.md)
- [Brand IP character system](references/brand-ip-character-system.md)
- [Packaging system](references/brand-packaging-system.md)
- [Brand application system](references/brand-application-system.md)
- [Ecommerce design](references/ecommerce-design.md)
- [Knowledge and education visuals](references/knowledge-education-visual.md)
- [Media creative](references/media-creative.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, API Calls]

**Output Format:** [Chinese prompt guidance and image generation or editing tool-call parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes requests to product-specific references, may ask 1-3 clarification questions, and uses existing image assets for consistency when available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
