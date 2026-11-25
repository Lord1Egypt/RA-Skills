## Description:

Detects whether image, video, or audio media is AI-generated and reports confidence scores, possible deepfakes, and likely generator models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other users can submit image, video, or audio media to check for AI generation, visual deepfakes, and likely generator models. The skill returns confidence scores to support review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has partial coverage and medium confidence; the reported login operation and claimed media-detection capability were not connected in the supplied evidence, and referenced files were unavailable to the scan.

Mitigation: Review the CLI behavior and unavailable references before installation, and submit only media appropriate for processing by dLazy's hosted service.

## Reference(s):

- [dLazy CLI project page (metadata link)](https://github.com/dlazy-ai/cli)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON result with a human-readable summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes confidence scores and detection labels; supports image, video, and audio only, not text. Requires a dLazy API key.]

## Skill Version(s):

1.0.44 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
