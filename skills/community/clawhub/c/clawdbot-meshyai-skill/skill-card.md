## Description: <br>
Use the Meshy.ai REST API to generate text-to-image and image-to-3D assets, poll async tasks, and download the results locally with MESHY_API_KEY authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sabatesduran](https://clawhub.ai/user/sabatesduran) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to create Meshy text-to-image outputs and image-to-3D OBJ assets, poll Meshy tasks until completion, and save generated files locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected images are sent to Meshy.ai under the user's Meshy account. <br>
Mitigation: Use the skill only for inputs that may be shared with Meshy.ai under that account's terms and access controls. <br>
Risk: Changing MESHY_BASE_URL can redirect API calls away from the default Meshy endpoint. <br>
Mitigation: Keep the default Meshy endpoint unless the alternate endpoint is deliberately trusted. <br>
Risk: Generated images and model files are written to the selected local output directory. <br>
Mitigation: Choose an output directory appropriate for generated assets and review files before reuse or distribution. <br>


## Reference(s): <br>
- [Meshy API notes](references/api-notes.md) <br>
- [Meshy API documentation](https://docs.meshy.ai/en) <br>
- [Meshy Text to Image API](https://docs.meshy.ai/en/api/text-to-image) <br>
- [Meshy Image to 3D API](https://docs.meshy.ai/en/api/image-to-3d) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands and local generated asset file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated files may include PNG images, OBJ models, and optional MTL materials saved under the selected output directory.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
