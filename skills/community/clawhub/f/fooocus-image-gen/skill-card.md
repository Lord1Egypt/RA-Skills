## Description: <br>
Local AI image generation using Fooocus (Stable Diffusion XL). Use when users want to generate images locally without relying on cloud APIs. Supports text-to-image, image variations, upscaling, inpainting, outpainting, face swap, and style transfer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wszhhx](https://clawhub.ai/user/wszhhx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to run local Fooocus-based SDXL image generation workflows, including text-to-image, variations, upscaling, inpainting, outpainting, face swap, and style transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup and startup scripts download third-party code, install Python packages, and can run local services. <br>
Mitigation: Install in a virtual environment, review commands before execution, and use only verified Fooocus installation paths. <br>
Risk: The local Fooocus service can create exposure if bound beyond localhost or shared externally. <br>
Mitigation: Keep Fooocus bound to localhost and avoid --listen or --share unless the user understands the network exposure. <br>
Risk: The --force reinstall path can delete an existing Fooocus directory. <br>
Mitigation: Use --force only after confirming the target path is the intended Fooocus install directory. <br>
Risk: Untrusted path or preset values can affect local script behavior. <br>
Mitigation: Use trusted local paths and known presets; do not pass unreviewed values from untrusted sources. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wszhhx/fooocus-image-gen) <br>
- [Fooocus project](https://github.com/lllyasviel/Fooocus) <br>
- [Fooocus wiki](https://github.com/lllyasviel/Fooocus/wiki) <br>
- [Fooocus API reference](references/fooocus_api.md) <br>
- [Fooocus parameters guide](references/parameters_guide.md) <br>
- [Fooocus presets reference](references/presets.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local image files through Fooocus when the local service and dependencies are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
