## Description: <br>
Uses the DMXAPI CLI to send image files or URLs to multimodal vision models for image description, OCR, chart analysis, object detection, and scene understanding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onee-io](https://clawhub.ai/user/onee-io) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to choose a vision model, construct DMXAPI CLI commands, and return image-recognition results for descriptions, OCR, chart extraction, object identification, scene analysis, and screenshot understanding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and prompts may leave the user's device for DMXAPI or downstream model processing. <br>
Mitigation: Submit only images the user is authorized to process, and avoid IDs, contracts, medical records, financial screenshots, faces, and other confidential content unless the user accepts that external processing. <br>
Risk: The workflow depends on installing and configuring the external dmxapi-cli package with an API key. <br>
Mitigation: Install the CLI only from a trusted source, configure the API key through the CLI as documented, and avoid exposing credentials in prompts, shared files, or command transcripts. <br>


## Reference(s): <br>
- [DMXAPI Console](https://www.dmxapi.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and model-returned text, Markdown, or JSON results depending on the prompt.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 20+, dmxapi-cli, a configured DMXAPI API key, and a local image path or remote image URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
