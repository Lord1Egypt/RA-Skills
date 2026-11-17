## Description:

Generate high-quality images from text prompts using BytePlus Seedream models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raezhliu](https://clawhub.ai/user/raezhliu)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and creative teams use this skill to generate images from text prompts, transform reference images, and create batches of visual assets through BytePlus Seedream models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference-image URLs, and generated-image requests are sent to BytePlus Seedream.

Mitigation: Use the skill only for content that can be shared with BytePlus under the user's applicable terms and data-handling requirements.

Risk: An endpoint override could route API keys and prompts to an untrusted server.

Mitigation: Keep ARK_DOLA_API_BASE unset or verify that it points to a trusted BytePlus HTTPS endpoint before running the skill.

Risk: The BytePlus API key can be exposed or abused if used in an untrusted environment.

Mitigation: Protect and quota-limit ARK_DOLA_API_KEY, and rotate it if it may have been used outside a trusted environment.

## Reference(s):

- [Dola Seedream on ClawHub](https://clawhub.ai/raezhliu/skills/dola-seedream)
- [BytePlus ModelArk Seedream Documentation](https://docs.byteplus.com/en/docs/ModelArk/1399008)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python API examples, shell commands, and JSON-style image generation results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated image results may be returned as URLs or base64 JSON depending on response_format.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
