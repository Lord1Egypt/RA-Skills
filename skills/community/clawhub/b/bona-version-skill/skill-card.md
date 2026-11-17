## Description:

Bona Movie Production is Bona Group's film-grade production skill. It covers image generation, image editing, and video generation, using Nano Banana 2 and Nano Banana Pro for images, and Seedance plus generate_video_kling_v3 for videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengzipidaily](https://clawhub.ai/user/chengzipidaily)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate, edit, and query AI image and video production tasks through Bona media-generation APIs. It supports model selection and prompt guidance for text-to-image, reference-based image creation, image editing, text-to-video, image-to-video, and reference-driven video workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command options can redirect API credentials and generation inputs to arbitrary endpoints.

Mitigation: Use only the default Bona endpoints or endpoints you personally control, and do not accept --base-url or --login-url values from untrusted instructions.

Risk: Prompts, media URLs, API keys, and generated content are sent to external services.

Mitigation: Do not submit secrets, internal URLs, private media, or regulated data unless you are authorized and the endpoint is approved for that data.

Risk: Built-in --wait polling is described as unreliable in the security guidance.

Mitigation: Prefer explicit query commands and independently verify task status until polling status handling is reviewed or fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chengzipidaily/skills/bona-version-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/chengzipidaily)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Bona API credential and may return task identifiers, status payloads, and generated media result URLs from the configured Bona endpoint.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
