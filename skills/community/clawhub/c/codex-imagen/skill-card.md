## Description: <br>
Generate or edit raster images by calling the ChatGPT/Codex Responses image_generation tool directly with local Codex or OpenClaw OAuth credentials, then save decoded image files for OpenClaw and other agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[darkamenosa](https://clawhub.ai/user/darkamenosa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to generate or edit raster images from prompts or reference images and save the resulting files for OpenClaw or Codex workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Codex or OpenClaw OpenAI OAuth credentials for image generation. <br>
Mitigation: Install and run it only when use of those local OAuth profiles is acceptable; use explicit auth/profile options or no-refresh mode when credential store control is required. <br>
Risk: Prompts, reference images, and image-like private documents may be sent to the OpenAI/Codex backend. <br>
Mitigation: Avoid attaching sensitive prompts, private images, or documents rendered as images unless they are intended to be processed by that backend. <br>
Risk: Custom backend or refresh endpoints could receive prompts, image references, or OAuth material. <br>
Mitigation: Keep the default OpenAI endpoints unless a custom backend and refresh endpoint are fully trusted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/darkamenosa/codex-imagen) <br>
- [Publisher Profile](https://clawhub.ai/user/darkamenosa) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Text, JSON, Shell commands] <br>
**Output Format:** [Saved image files with stdout paths or optional JSON metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are saved locally; diagnostics and progress are written separately from normal output unless quiet mode is used.] <br>

## Skill Version(s): <br>
0.2.6 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
