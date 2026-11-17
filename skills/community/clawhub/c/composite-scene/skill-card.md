## Description:

Merge several real images into one coherent picture without manual cut-out or masking, using separate reference images and prompts that specify placement, scale, lighting, and relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to guide agents through combining products, subjects, scenes, or style references into coherent generated images with matched lighting and perspective.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided reference images or image URLs may be sent to the configured image-generation service.

Mitigation: Avoid sensitive private images unless the provider and workspace policy are acceptable for the use case.

Risk: Composite outputs can mismatch placement, scale, lighting, identity, or perspective.

Mitigation: Review generated results against the requested relationships and retry with clearer references or more explicit prompts.

Risk: Generated composites can introduce unsupplied logos, badges, or on-image copy.

Mitigation: Inspect outputs for invented brand elements or text and reject or regenerate results that add unsupported details.

## Reference(s):

- [Worked recipes](artifact/references/examples.md)
- [Composite Scene ClawHub page](https://clawhub.ai/runware/skills/composite-scene)

## Skill Output:

**Output Type(s):** [guidance, configuration, code]

**Output Format:** [Markdown guidance with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image-generation request shapes that reference user-provided images or image URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
