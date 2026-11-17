## Description:

Analyzes a reference advertisement into a shot breakdown and prompt, then helps create a new video through an editable draft flow or inspect the source without generating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsturbo](https://clawhub.ai/user/adsturbo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and creators use this skill to analyze an advertisement's shots and prompts, adapt the structure, and request a new video, or to inspect a video without generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded media may be reachable through a public link.

Mitigation: Before uploading, check that the media is intended to be shared by public URL and remove sensitive content that should remain private.

Risk: Submitting a video generation can charge account credits, and the confirmation step may not be reliable in every case.

Mitigation: Review the draft and displayed quote, then obtain the user's explicit confirmation immediately before submitting the credit-charging request.

Risk: The security scan covered 11 of 12 components, so its evidence is incomplete.

Mitigation: Review the unscanned component before relying on the scan as a complete assessment.

## Reference(s):

- [Ad Clone Guide](references/ad_clone.md)
- [Media Upload Guide](references/upload.md)
- [Login Guide](references/login.md)
- [Async Task Guide](references/work.md)
- [AdsTurbo Pricing](https://adsturbo.ai/pricing)
- [AdsTurbo API Key Management](https://adsturbo.ai/iris/api)

## Skill Output:

**Output Type(s):** [Analysis, Prompts, Guidance, Video links]

**Output Format:** [Structured shot analysis and prompts, with generated video links when a video is created]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return analysis only or a generated video result; generated clips follow the service's duration and account limits.]

## Skill Version(s):

1.4.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
