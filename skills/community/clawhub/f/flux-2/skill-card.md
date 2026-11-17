## Description:

Generate and edit photoreal images with Black Forest Labs FLUX.2 (Max, Pro, Flex, Dev) and FLUX 3 Klein through the PopNow API, including LoRA variants and exact brand colors. Exact USD quotes before any charge. Use when the user asks for FLUX, Black Forest Labs, photorealism or LoRA image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyuminjo](https://clawhub.ai/user/kyuminjo)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users and developers can create or edit photoreal images with FLUX.2 and FLUX 3 Klein, including LoRA styles and precise brand colors, through PopNow. The workflow obtains an exact USD quote before creating a paid generation task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image generation uses a paid PopNow API balance.

Mitigation: Approve the exact quoted maximum cost before generation, and use a dedicated key with model and spending restrictions.

Risk: Prompts and reference media URLs are sent to PopNow and its generation provider; command arguments may remain in host logs.

Mitigation: Avoid sensitive material and review prompt and reference content before sending it.

Risk: Provider retention and billing behavior were not independently tested.

Mitigation: Review provider policies and monitor API usage.

## Reference(s):

- [PopNow FLUX.2 Max model page](https://popnow.ai/models/flux-2-max)
- [PopNow task API documentation](https://popnow.ai/docs/tasks)

## Skill Output:

**Output Type(s):** [Images, Text]

**Output Format:** [Generated image links with concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model-specific image settings, including LoRA options where supported, follow the selected model's schema.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
