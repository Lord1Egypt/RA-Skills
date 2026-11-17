## Description:

Generate, remix, and edit images using fal.ai models for text-to-image creation, image-to-image remixing, and targeted inpainting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delorenj](https://clawhub.ai/user/delorenj)

### License/Terms of Use:


## Use Case:

Developers, designers, and content teams use this skill to create new images, transform source images, and perform targeted masked edits through fal.ai model workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, source images, and masks are sent to fal.ai for generation and editing.

Mitigation: Avoid private or regulated images unless fal.ai data handling has been reviewed for the intended use.

Risk: Generated images may store prompt, model, and parameter details in image metadata.

Mitigation: Review or strip image metadata before sharing outputs that involve sensitive prompts or sources.

Risk: Runtime dependencies are declared with version ranges rather than a locked production dependency set.

Mitigation: Use locked dependencies before production deployment.

## Reference(s):

- [Model Comparison](references/model-comparison.md)
- [Usage Examples](references/usage-examples.md)
- [fal.ai Documentation](https://docs.fal.ai/)
- [fal.ai Model Playground](https://fal.ai/explore/search)
- [fal.ai API Keys](https://fal.ai/dashboard/keys)
- [fal.ai Pricing](https://fal.ai/pricing)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated image file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images may include prompt, model, and parameter metadata.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
