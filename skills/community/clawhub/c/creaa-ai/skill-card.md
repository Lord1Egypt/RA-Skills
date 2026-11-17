## Description:

Creaa AI generates and edits images and generates videos through the Creaa.ai API, supporting text-to-image, image editing, text-to-video, and image-to-video workflows across multiple AI models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yys2024](https://clawhub.ai/user/yys2024)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and external users use this skill to generate or edit image and video assets through Creaa.ai API calls from an agent or terminal workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, image URLs, base64 image data, task metadata, and generated results are handled by Creaa.ai.

Mitigation: Avoid submitting secrets, regulated data, or sensitive personal or business media unless third-party processing through Creaa.ai is approved.

Risk: Requests may spend Creaa.ai API credits.

Mitigation: Confirm model pricing and available API credits before running generation or edit requests.

Risk: CREAA_API_KEY is required for API access.

Mitigation: Protect CREAA_API_KEY like any other credential and avoid exposing it in shared logs, prompts, or code.

## Reference(s):

- [Creaa.ai](https://creaa.ai)
- [Creaa.ai profile API keys](https://creaa.ai/profile)
- [Creaa.ai pricing](https://creaa.ai/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREAA_API_KEY; generated media is returned through asynchronous Creaa.ai task result URLs.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
