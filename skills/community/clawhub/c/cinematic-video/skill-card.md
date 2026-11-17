## Description:

Make video that looks shot, not generated, with deliberate framing, lens, camera motion, lighting, and color grade.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runware](https://clawhub.ai/user/runware)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn text briefs or source stills into short cinematic video generation requests with deliberate framing, camera motion, lighting, and color grading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and source images used for image-to-video generation may be sent to the configured video provider.

Mitigation: Use only prompts and media that are appropriate for the provider's privacy terms, cost model, and generated-video rights.

Risk: Provider model schemas, dimensions, durations, and supported image inputs can change over time.

Mitigation: Confirm the live model schema before submitting generation requests.

## Reference(s):

- [Cinematic video worked recipes](artifact/references/examples.md)
- [Cinematic Video on ClawHub](https://clawhub.ai/runware/skills/cinematic-video)
- [runware publisher profile](https://clawhub.ai/user/runware)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with cinematic prompt text and JSON videoInference examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require asynchronous video generation and polling before a provider video URL is available.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
