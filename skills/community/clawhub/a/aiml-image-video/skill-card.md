## Description:

Generate images or videos via AIMLAPI from prompts, including image-to-image and image-to-video flows through helper scripts with retries, User-Agent headers, and async video polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aimlapihello](https://clawhub.ai/user/aimlapihello)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to generate image and video assets through AIMLAPI from text prompts or starting images. It is suited to workflows that need reusable command examples, media-generation scripts, and troubleshooting guidance for AIMLAPI image and video endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, parameters, and explicitly provided local image inputs may be sent to AIMLAPI.

Mitigation: Avoid sensitive prompts and private files; use the skill only in environments where AIMLAPI is approved to receive that data.

Risk: Remote API responses are trusted when downloading generated media, creating avoidable network and file-write exposure.

Mitigation: Run with a constrained output directory and restricted network environment until media URL validation, bounded downloads, and safe video filename generation are added.

Risk: The skill requires an AIMLAPI API key and supports loading it from a file path.

Mitigation: Store the API key securely, pass only intended key files, and review command arguments before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aimlapihello/skills/aiml-image-video)
- [AIMLAPI media notes](references/aimlapi-media.md)
- [Image-to-image generation](references/IMAGE-TO-IMAGE.md)
- [Image-to-video generation](references/IMAGE-TO-VIDEO.md)
- [AIMLAPI image API base URL](https://api.aimlapi.com/v1)
- [AIMLAPI video API base URL](https://api.aimlapi.com/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples; generated media is written as image or video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AIMLAPI_API_KEY and may send prompts, selected parameters, and explicitly provided image inputs to AIMLAPI.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
