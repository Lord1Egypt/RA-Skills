## Description:

Generate images using Azure OpenAI DALL-E. Supports batch generation, custom prompts, and outputs a gallery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhibavishi](https://clawhub.ai/user/abhibavishi)

### License/Terms of Use:


## Use Case:

Developers and content creators use this skill to generate Azure OpenAI DALL-E images from prompts, including batch image generation, custom size and quality settings, and local gallery output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Azure API key can be sent to an unvalidated endpoint if AZURE_OPENAI_ENDPOINT is set incorrectly or maliciously.

Mitigation: Install only from a trusted skill directory and verify AZURE_OPENAI_ENDPOINT is the intended Azure HTTPS endpoint before running the generator.

Risk: Generated gallery HTML may include unescaped prompt text.

Mitigation: Avoid sharing generated galleries from untrusted prompts until HTML escaping is fixed or independently sanitize prompt text before publishing.

Risk: Manifest and gallery files can retain prompt history.

Mitigation: Treat generated manifest and gallery files as sensitive when prompts may contain confidential or private information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhibavishi/skills/azure-image-gen)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, plus generated PNG files, manifest JSON, and an HTML gallery when run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Azure OpenAI endpoint, API key, and DALL-E deployment environment variables.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
