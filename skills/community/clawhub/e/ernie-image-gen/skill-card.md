## Description:

Baidu ERNIE-Image text-to-image generation skill for creating local PNG images through Baidu AI Studio's ERNIE-Image and ERNIE-Image-Turbo models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiwork4me](https://clawhub.ai/user/aiwork4me)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate images from Chinese or English prompts with Baidu AI Studio ERNIE-Image models, including batch generation, size selection, seed control, and local PNG output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and generation parameters are sent to Baidu AI Studio, and the Python process reads AI_STUDIO_API_KEY from the environment.

Mitigation: Do not include secrets, private personal data, or confidential business data in prompts; run the skill only where exposing the Baidu API key to the process is acceptable.

Risk: The documented uv installation path includes an unverified curl-to-shell command.

Mitigation: Install uv through a trusted and verified channel before using the skill.

Risk: Runtime dependency resolution uses an unpinned lower-bound openai dependency.

Mitigation: Pin or lock the openai dependency in the execution environment before production use.

Risk: Generated files are written to a local output directory.

Mitigation: Confirm the output directory before generation and run the skill in a constrained workspace.

## Reference(s):

- [ERNIE-Image API Reference](references/api-guide.md)
- [Baidu AI Studio API endpoint](https://aistudio.baidu.com/llm/lmapi/v3)
- [Baidu AI Studio access token page](https://aistudio.baidu.com/account/accessToken)
- [ClawHub skill page](https://clawhub.ai/aiwork4me/skills/ernie-image-gen)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Guidance]

**Output Format:** [Local PNG image files with MEDIA path lines; optional structured JSON result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates 1-4 images per request, supports seven image sizes, seed control, prompt enhancement, inference steps, guidance scale, and non-overwriting filename suffixes.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
