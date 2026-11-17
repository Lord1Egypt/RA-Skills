## Description:

Generate images using Cloudflare Workers AI flux-1-schnell model. Use when user requests image generation with text-to-image using Cloudflare Workers API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[expysf98](https://clawhub.ai/user/expysf98)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate PNG images from text prompts through Cloudflare Workers AI and return the saved image path for delivery to a user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports an exposed Cloudflare token.

Mitigation: Remove and rotate the token before installation, and load credentials from user-controlled secret storage.

Risk: The security evidence reports that crafted prompts can reach shell execution.

Mitigation: Replace shell-based curl execution with a native HTTPS client or a shell-free argument list.

Risk: The security guidance identifies fixed temporary response files and unclear data handling.

Mitigation: Avoid fixed temporary file paths and document where generated images are saved and what prompt data is sent to Cloudflare.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/expysf98/skills/cloudflare-image-gen)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Files]

**Output Format:** [PNG image file with a text file path returned by the script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts are sent to Cloudflare Workers AI; generated images are saved as PNG files.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
