## Description:

Controlled Generation helps an agent keep the composition of a source image while changing the generated image's style, subject, material, or finish.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and creative operators use this skill to generate controlled image variations that preserve a source image's pose, outline, depth, or scene regions while changing the visual outcome.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source images may be processed by an external Runware service.

Mitigation: Do not use confidential, regulated, private, or proprietary images unless the user has reviewed and accepted the service's retention and access terms.

Risk: Image-generation schemas and model availability can change over time.

Mitigation: Confirm model status and schema-valid fields before making Runware calls.

## Reference(s):

- [Controlled Generation worked recipes](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/runware/skills/controlled-generation)

## Skill Output:

**Output Type(s):** [Guidance, JSON, API calls]

**Output Format:** [Markdown guidance with JSON request examples and Runware image response URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides a two-step external image-processing workflow: control-map extraction followed by conditioned image generation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
