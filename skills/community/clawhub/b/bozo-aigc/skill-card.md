## Description:

Generates images from text prompts or one to eight reference image URLs using the BizyAir GPT_IMAGE_2 API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bozoyan](https://clawhub.ai/user/bozoyan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request text-to-image or image-to-image generation with selectable aspect ratios. The agent runs the appropriate script, waits for the BizyAir response, downloads the generated image, and reports the saved file path.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference image URLs, and BizyAir API authorization are sent to the BizyAir endpoint.

Mitigation: Install only when this data sharing is acceptable for the intended users and content.

Risk: The skill handles API credentials and logs an API-key prefix during execution.

Mitigation: Remove API-key-prefix logging before use and keep BIZYAIR_API_KEY in a protected environment variable.

Risk: The scripts download remote image content and save it locally.

Mitigation: Validate downloaded files before saving or opening them.

Risk: The bundled permission guidance allows broad chmod usage.

Mitigation: Narrow chmod permission to the exact scripts that need execute permissions.

Risk: The security verdict is suspicious because credentials and downloaded remote content are handled unsafely enough to require review.

Mitigation: Review the skill and apply the security guidance before installing or running it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bozoyan/skills/bozo-aigc)
- [BizyAir webapp task API endpoint](https://api.bizyair.cn/w/v1/webapp/task/openapi/create)
- [ClawHub publisher profile](https://clawhub.ai/user/bozoyan)

## Skill Output:

**Output Type(s):** [shell commands, files, guidance]

**Output Format:** [Markdown guidance with bash command execution and saved image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved under pic/ with timestamped filenames; requests may take 90 seconds to 10 minutes.]

## Skill Version(s):

2.0.0 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
