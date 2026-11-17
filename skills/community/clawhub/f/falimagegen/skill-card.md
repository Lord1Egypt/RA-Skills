## Description:

Call fal.ai model APIs for image generation (text-to-image and image-to-image). Use when a user asks to integrate fal, construct requests, run jobs, handle auth, or return image URLs from fal model APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxmzdxxxm](https://clawhub.ai/user/xxmzdxxxm)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to integrate fal.ai image-generation model APIs, construct SDK or REST requests, validate model inputs, and return generated image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: fal.ai requests may send prompts, source images, and request metadata to an external service.

Mitigation: Use a scoped FAL key and avoid sending sensitive prompts or private images unless external processing is intended.

Risk: Model schemas and output fields vary across fal.ai models, so stale examples can produce failed or incorrect requests.

Mitigation: Confirm the selected model's current documentation before constructing requests and review generated calls before execution.

## Reference(s):

- [Fal Model API Checklist](references/fal-model-api-checklist.md)
- [fal Model API Examples](references/fal-model-examples.md)
- [fal Model APIs Quickstart](https://docs.fal.ai/model-apis/quickstart)
- [Generate Images from Text](https://docs.fal.ai/model-apis/guides/generate-images-from-text)
- [fal Client Libraries](https://docs.fal.ai/model-apis/client)
- [fal Model Endpoints](https://docs.fal.ai/model-apis/model-endpoints)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces request templates and response-handling guidance; generated API calls should be reviewed before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
