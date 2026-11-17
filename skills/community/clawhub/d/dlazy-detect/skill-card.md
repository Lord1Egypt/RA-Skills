## Description:

Detects whether image, video, or audio media is AI-generated, including visual deepfakes and likely generator attribution, and returns confidence scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use the skill to assess whether image, video, or audio media may be AI-generated or contain a visual deepfake, and to interpret the returned confidence scores and likely generator attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports that the inspected content appears to run a login command without showing the advertised detection workflow, and scan coverage is incomplete because local references were unresolved.

Mitigation: Review the complete installed package and confirm the commands it runs before use; begin with non-sensitive media until its behavior is verified.

Risk: The documented workflow uploads local media to dLazy storage or forwards public media URLs to a hosted detection service.

Mitigation: Use media only when you are authorized to share it with the service, especially when it contains personal or confidential information.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/dlazy-detect)
- [dLazy CLI project (metadata link; repository provenance unavailable)](https://github.com/dlazy-ai/cli)
- [dLazy CLI on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy](https://dlazy.com)
- [dLazy API key setup](https://dlazy.com/dashboard/organization/api-key)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured JSON verdict with confidence scores and a human-readable summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports media type, AI-generation and deepfake scores, boolean classifications, and likely generator attribution when available. Text input is unsupported.]

## Skill Version(s):

1.0.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
