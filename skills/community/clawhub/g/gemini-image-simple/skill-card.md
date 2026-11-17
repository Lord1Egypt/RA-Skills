## Description:

Generate and edit images with Gemini API using pure Python stdlib. Zero dependencies - works on locked-down environments where pip/uv aren't available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cluka-399](https://clawhub.ai/user/cluka-399)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate new images or edit existing images through Google's Gemini API in environments where installing Python packages is not practical.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and optional input images are sent to Google's Gemini API as part of image generation and editing.

Mitigation: Avoid confidential images, secrets, or sensitive prompt content unless external processing by Gemini is approved for the use case.

## Reference(s):

- [Google AI Studio API keys](https://aistudio.google.com/apikey)
- [ClawHub skill page](https://clawhub.ai/cluka-399/skills/gemini-image-simple)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Generated or edited image file with concise terminal status or error text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GEMINI_API_KEY and supports optional PNG, JPG, JPEG, GIF, or WEBP input images for editing.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
