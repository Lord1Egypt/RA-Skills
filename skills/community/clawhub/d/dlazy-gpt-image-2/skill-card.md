## Description:

GPT Image 2 model for text-to-image and image editing, including image synthesis and editing with reference inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate images from text prompts or edit and synthesize images using reference images through dLazy's hosted GPT Image 2 service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review had medium confidence and could not verify the external CLI's authentication, prompt, or media handling; prompts and local reference images are sent to dLazy's hosted service.

Mitigation: Review the CLI's authentication and data handling before use, and only submit prompts and images you are comfortable sending to the service. Use a dedicated API key and rotate or revoke it if needed.

## Reference(s):

- [ClawHub release](https://clawhub.ai/dlazyai/skills/dlazy-gpt-image-2)
- [dLazy CLI package on npm](https://www.npmjs.com/package/@dlazy/cli)
- [dLazy service](https://dlazy.com)
- [CLI repository listed in skill metadata](https://github.com/dlazy-ai/cli)

## Skill Output:

**Output Type(s):** [Images, JSON, Text]

**Output Format:** [Generated image files or hosted image URLs, with a JSON response envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports text prompts and up to five reference images; asynchronous mode can return a task identifier before results are ready.]

## Skill Version(s):

1.3.45 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
