## Description: <br>
Generate images with Doubao Seedream through Volcano Engine ARK when the user invokes Maliang or requests Doubao, Seedream, or Volcano ARK image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoannaXing](https://clawhub.ai/user/JoannaXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request text-to-image generation through Doubao Seedream, receive generated images in chat, and keep local image, manifest, and gallery outputs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts are sent to Volcano Engine ARK or another configured endpoint. <br>
Mitigation: Use a limited API key and avoid secrets or sensitive personal or business data in prompts. <br>
Risk: A custom SEEDREAM_API_ENDPOINT can redirect prompt and API-key-bearing requests. <br>
Mitigation: Verify any custom endpoint before use and prefer the documented ARK image generation endpoint. <br>
Risk: Generated images, manifests, and gallery files are retained locally. <br>
Mitigation: Review and periodically delete saved output folders when local retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JoannaXing/doubao-maliang-image-gen) <br>
- [OpenClaw homepage metadata](https://github.com/JoannaXing/doubao-maliang-image-gen) <br>
- [Volcano Engine ARK Console](https://console.volcengine.com/ark/) <br>
- [Volcano Engine ARK image generation endpoint](https://ark.cn-beijing.volces.com/api/v3/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, Configuration instructions, Shell commands] <br>
**Output Format:** [Generated image files with JSON manifest, local HTML gallery, and text path summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Volcano Engine API key; supports configurable model, endpoint, image count, size, and output directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
