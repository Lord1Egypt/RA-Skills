## Description:

Generates and edits images through API易's GPT Image 2 service, including text-to-image, image editing, multi-image fusion, size and quality controls, and PNG/JPEG/WebP output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent to generate new images, edit uploaded images, or fuse multiple reference images through the API易 GPT Image 2 service with CLI-exposed size, quality, and output-format controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and uploaded images are sent to api.apiyi.com for generation or editing.

Mitigation: Install only if that data sharing is acceptable for the intended content and users.

Risk: The skill can incur paid API calls through API易.

Mitigation: Use it in an environment with billing controls and review size, quality, and iteration settings before repeated runs.

Risk: Command templates combine user prompts, filenames, and shell examples, which can be risky if rendered directly into a shell command.

Mitigation: Pass arguments as arrays through the agent runtime, prefer APIYI_API_KEY over command-line keys, and avoid shell metacharacters in prompts and filenames.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/skills/apiyi-gpt-image-2-gen)
- [Publisher profile](https://clawhub.ai/user/wuchubuzai2018)
- [API易 service](https://api.apiyi.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, configuration, guidance]

**Output Format:** [Markdown or text responses with CLI commands and generated image file paths; scripts write PNG, JPEG, or WebP files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIYI_API_KEY or an explicit API key argument; supports prompt, optional input images, size, quality, output format, and output compression parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
