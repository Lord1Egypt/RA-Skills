## Description:

Fotor AI image generator and AI video generator for photo editing, background remover, background replacement, product photos, ad creatives, social media graphics, poster and banner design, image upscaling, photo restoration, portrait enhancement, text-to-video, and image-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fotor-everimaging](https://clawhub.ai/user/fotor-everimaging)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content teams use this skill to create or edit images and videos for e-commerce, marketing, branding, social media, and content production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup and runtime behavior can install or update dependencies and interact with Fotor services using user credentials.

Mitigation: Review the setup path before installation and prefer pinned or verified installs over latest-version upgrade commands.

Risk: The skill sends prompts and uploaded media to Fotor and can produce signed or reusable media URLs in command output.

Mitigation: Use a dedicated Fotor API key, treat prompts and media as shared with Fotor, and keep command logs private.

Risk: Custom endpoints can route credentials and media to a non-default service.

Mitigation: Avoid custom endpoints unless the endpoint is fully trusted and intentionally configured.

## Reference(s):

- [Fotor Skills GitHub Homepage](https://github.com/fotor-ai/fotor-skills)
- [Fotor Skills Developer Documentation](https://developers.fotor.com/fotor-skills/)
- [ClawHub Skill Page](https://clawhub.ai/fotor-everimaging/skills/fotor-skills)
- [Image Models](references/image_models.md)
- [Video Models](references/video_models.md)
- [Parameter Reference](references/parameter_reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON task specifications, shell commands, and result URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return generated media URLs, uploaded media URLs, task status, error details, credit usage, and fallback model metadata.]

## Skill Version(s):

1.0.20 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
