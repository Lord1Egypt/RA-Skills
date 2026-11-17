## Description:

Generate coherent transition videos using Jimeng's first and tail frame models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to generate a transition video from a prompt and supplied first and last frame images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had medium confidence and partial coverage, and flagged a mismatch between the video-generation description and the reported authentication steps.

Mitigation: Review the dLazy CLI authentication and API-key setup before use, and inspect instructions that may be obscured by formatting.

Risk: Prompts and local image or media files supplied to the skill are sent to dLazy-hosted services for processing.

Mitigation: Submit only content approved for processing by dLazy, and consult the service terms before sending sensitive material.

## Reference(s):

- [dLazy](https://dlazy.com)
- [@dlazy/cli on npm](https://www.npmjs.com/package/@dlazy/cli)

## Skill Output:

**Output Type(s):** [Video files, Hosted media URLs, JSON]

**Output Format:** [Generated video asset with JSON result or task metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Videos are 5 or 10 seconds; generation can return immediately with an asynchronous task identifier.]

## Skill Version(s):

1.3.41 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
