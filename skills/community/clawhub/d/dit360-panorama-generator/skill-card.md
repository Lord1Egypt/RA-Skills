## Description: <br>
Generates 360-degree panorama images with the DiT360 model, converts outputs to JPG, and creates an interactive viewer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative users can use this skill to generate equirectangular 360-degree panorama images from text prompts and preview them in a browser-based panorama viewer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Panorama prompts are sent to the Hugging Face DiT360 Space. <br>
Mitigation: Do not include secrets, personal data, or proprietary prompt text. <br>
Risk: The launcher installs the gradio_client Python dependency at runtime. <br>
Mitigation: Review the dependency install command and run it only in an environment where runtime package installation is acceptable. <br>
Risk: The generated viewer loads Pannellum assets from jsdelivr and may leave a local server running on port 8899. <br>
Mitigation: Use the viewer only where external CDN assets are acceptable and stop the local server after viewing if the port should not remain open. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/dit360-panorama-generator) <br>
- [DiT360 GitHub repository](https://github.com/Insta360-Research-Team/DiT360) <br>
- [DiT360 Hugging Face Space](https://huggingface.co/spaces/Insta360-Research/DiT360) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates WebP and JPG panorama files plus a viewer.html file, and may start a local HTTP server on port 8899.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
