## Description:

Swap out one element of a video: replace the on-screen person, drive a static portrait with a reference video's motion, or translate the whole video into another language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsturbo](https://clawhub.ai/user/adsturbo)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to replace a person in a video, apply motion from a reference clip to a still portrait, or translate and redub a video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The upload workflow may put personal images, recordings, or videos behind publicly accessible links without a warning or consent step.

Mitigation: Before uploading, confirm the user is comfortable with public access and has consent to share the media.

Risk: The security scan assessed 11 of 12 components, so coverage is partial; its suspicious verdict is a review signal rather than a finding of malicious intent.

Mitigation: Review the skill and its upload behavior before use, keeping the partial scan coverage in mind.

## Reference(s):

- [Login and account setup](references/login.md)
- [Uploading media](references/upload.md)
- [Video transformation options](references/video_transform.md)
- [Async task handling](references/work.md)
- [AdsTurbo pricing](https://adsturbo.ai/pricing)
- [AdsTurbo API key management](https://adsturbo.ai/iris/api)
- [ClawHub skill release](https://clawhub.ai/adsturbo/skills/adsturbo-video-transform)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Video links]

**Output Format:** [Natural language guidance and generated video URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video transformations run asynchronously and are billed in credits.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
