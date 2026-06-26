## Description: <br>
AI image generation skill for creating, editing, and merging images with APIYI's gpt-image-2-all service, with Chinese prompt support and command-line helpers for Node.js and Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuchubuzai2018](https://clawhub.ai/user/wuchubuzai2018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate new images, edit existing images, or merge multiple image references through APIYI's gpt-image-2-all API. It is intended for workflows where prompts, optional input images, and API credentials can be sent to APIYI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, API keys, and any images selected for editing are sent to APIYI's remote paid API. <br>
Mitigation: Install only if the publisher and APIYI are trusted for the intended data, use APIYI_API_KEY instead of command-line keys, and avoid private or sensitive images unless APIYI's terms are acceptable. <br>
Risk: Generated URL outputs may be temporary. <br>
Mitigation: Download or store generated images promptly when durable retention is required. <br>


## Reference(s): <br>
- [APIYI platform](https://api.apiyi.com/) <br>
- [ClawHub skill page](https://clawhub.ai/wuchubuzai2018/apiyi-gpt-image-2-all-gen) <br>
- [Publisher profile](https://clawhub.ai/user/wuchubuzai2018) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated image files or image URLs/base64 data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIYI_API_KEY or an explicit API key argument; image URL outputs may be temporary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
