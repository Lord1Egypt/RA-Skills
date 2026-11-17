## Description:

Agnes Vision lets an agent send local images to Agnes's agnes-2.0-flash multimodal API for image description, OCR, recognition, and comparison.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruokkkkk](https://clawhub.ai/user/ruokkkkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when they specifically need image understanding results from the Agnes agnes-2.0-flash service, including OCR, image description, object recognition, chart extraction, and multi-image comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a plaintext API key in config.json.

Mitigation: Remove the packaged config.json key before use, rotate the exposed credential, and prefer AGNES_API_KEY or a runtime --key value.

Risk: The skill uploads image contents to a third-party Agnes API endpoint.

Mitigation: Use the skill only with images that are approved for upload to that service and avoid sensitive, confidential, or regulated image data unless policy permits it.

Risk: The API endpoint is configurable.

Mitigation: Keep the endpoint set to an explicitly trusted HTTPS service and review any endpoint override before execution.

## Reference(s):

- [Agnes API chat completions endpoint](https://apihub.agnes-ai.com/v1/chat/completions)
- [ClawHub skill page](https://clawhub.ai/ruokkkkk/skills/agnes-vision)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown synthesized from the model response, with optional shell commands and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying script prints the model answer to stdout and sends errors to stderr; max output tokens can be configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
