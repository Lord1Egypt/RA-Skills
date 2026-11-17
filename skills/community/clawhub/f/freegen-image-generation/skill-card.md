## Description:

Freegen image-gen API: TXT2IMG, I2I, Inpainting, RemoveBG, Upscale via local freegen container. Supports Flux, SDXL, SD1.5, Lightning models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runtanplan22](https://clawhub.ai/user/runtanplan22)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate and edit images through a local freegen service that wraps Dezgo APIs for text-to-image, image-to-image, inpainting, background removal, upscaling, and related image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags that the skill describes routing restricted prompts through an unfiltered model.

Mitigation: Review the skill before installation when content-safety guarantees are required, and do not use it to bypass provider or platform safety rules.

Risk: Prompts and images may be processed by the local freegen service and Dezgo.

Mitigation: Avoid sending sensitive, personal, regulated, or confidential prompts or images unless that processing is acceptable for the deployment.

## Reference(s):

- [Dezgo](https://dezgo.com)
- [ClawHub skill page](https://clawhub.ai/runtanplan22/skills/freegen-image-generation)
- [ClawHub publisher profile](https://clawhub.ai/user/runtanplan22)

## Skill Output:

**Output Type(s):** [guidance, code, API Calls, configuration]

**Output Format:** [Markdown with JSON and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompts, request payloads, endpoint guidance, and image workflow instructions for a local freegen service.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
