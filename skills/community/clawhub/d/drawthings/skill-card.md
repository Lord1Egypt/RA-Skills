## Description: <br>
Generate images with DrawThings (Stable Diffusion) via a local Automatic1111-compatible API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dustinparsons](https://clawhub.ai/user/dustinparsons) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, designers, and other external users use this skill to generate single or batched images from text prompts through a local DrawThings service, tune generation parameters, and save image outputs with metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and generation parameters may be stored in generated PNG or JSON metadata and later shared unintentionally. <br>
Mitigation: Avoid using secrets, private client data, or regulated information in prompts, and review output metadata before sharing generated files. <br>
Risk: The skill sends prompts to the configured DrawThings service and writes generated files locally. <br>
Mitigation: Install it only when you intend to use a trusted local DrawThings service, verify DRAWTHINGS_URL, and choose output paths deliberately. <br>


## Reference(s): <br>
- [DrawThings API Reference](references/api-reference.md) <br>
- [Recommended Models for DrawThings](references/models.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dustinparsons/drawthings) <br>
- [CivitAI](https://civitai.com) <br>
- [Hugging Face Models](https://huggingface.co/models) <br>


## Skill Output: <br>
**Output Type(s):** [Images, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [PNG image files with optional JSON metadata and terminal status text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a reachable local DrawThings API via DRAWTHINGS_URL; generated prompts and parameters may be embedded in PNG or JSON metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
