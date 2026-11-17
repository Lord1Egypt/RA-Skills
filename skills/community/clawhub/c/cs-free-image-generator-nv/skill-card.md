## Description:

Uses NVIDIA's image-generation API to turn text prompts into image responses and save the returned JSON with base64 image data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[savior1987](https://clawhub.ai/user/savior1987)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate images from text prompts through NVIDIA's image-generation API and keep the response JSON for later decoding or review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and generated output metadata are sent to NVIDIA's API.

Mitigation: Avoid sensitive or regulated prompts unless the deployment is approved for that data.

Risk: Full response JSON is stored under /tmp/cs-free-image-generator/nv/.

Mitigation: Review file permissions and retention, or move outputs to private storage for production use.

Risk: The skill reads NVIDIA_API_KEY from ~/.openclaw/.env.

Mitigation: Keep ~/.openclaw/.env limited to necessary secrets and protect it with appropriate local permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/savior1987/skills/cs-free-image-generator-nv)
- [NVIDIA Flux.2 Klein 4B image-generation endpoint](https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.2-klein-4b)

## Skill Output:

**Output Type(s):** [API Calls, Files, JSON]

**Output Format:** [JSON response printed to stdout and saved as a timestamped JSON file containing base64 image data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a prompt, width, and height; width and height are constrained to 1-4096 pixels.]

## Skill Version(s):

1.3.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
