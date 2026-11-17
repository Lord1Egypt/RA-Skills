## Description:

Generate videos from text, images, frame pairs, and reference media, and extend or locally edit existing clips.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsturbo](https://clawhub.ai/user/adsturbo)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and marketers use this skill to generate video clips from prompts or reference media, then extend or locally edit existing clips.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upload workflow may send selected local media to a third party and create publicly accessible links without first explaining this or asking for approval.

Mitigation: Explain what media will be uploaded and that its resulting link may be public, then get the user's approval before uploading; confirm the media is appropriate to share.

Risk: The security scan was partial and reported malformed manifest data and unresolved references, so the available evidence does not establish that the artifact is safe.

Mitigation: Resolve the manifest and reference issues and complete a review of all components before deployment.

## Reference(s):

- [Video generation options](references/video_generation.md)
- [Media upload guidance](references/upload.md)
- [Asynchronous task handling](references/work.md)
- [Account login](references/login.md)
- [AdsTurbo pricing](https://adsturbo.ai/pricing)

## Skill Output:

**Output Type(s):** [Video links, Text guidance]

**Output Format:** [Video URL with concise text response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video results are returned after asynchronous generation.]

## Skill Version(s):

1.4.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
