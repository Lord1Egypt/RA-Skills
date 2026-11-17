## Description:

Generate images using APIYI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengwuzhi](https://clawhub.ai/user/mengwuzhi)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to generate PNG images from natural-language prompts through APIYI and save them into a chosen workspace path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts are sent to APIYI for image generation.

Mitigation: Avoid sensitive prompt content and install only if APIYI use is acceptable for the intended workflow.

Risk: The skill stores and uses an APIYI API key.

Mitigation: Use APIYI_API_KEY from the environment and follow the security guidance to avoid the documented --api-key override until the key-handling issue is fixed.

Risk: Generated images are downloaded and written to local paths selected by the user.

Mitigation: Choose output paths deliberately and consider running the skill in a restricted environment with pinned dependencies.

## Reference(s):

- [Draw Images By Apiyi on ClawHub](https://clawhub.ai/mengwuzhi/skills/draw-images-by-apiyi)
- [APIYI](https://apiyi.com/)
- [APIYI OpenAI-compatible API endpoint](https://api.apiyi.com/v1)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [PNG image files with command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates one image per request at 1K, 2K, or 4K resolution and prints a MEDIA path when successful.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
