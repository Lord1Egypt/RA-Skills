## Description: <br>
Generate or edit images from text prompts or reference images with customizable sizes using the Agnes Image 2.1 Flash API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lg0219](https://clawhub.ai/user/lg0219) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate new images from prompts or edit an existing image by sending a URL, Data URI, or local file reference through Agnes Image 2.1 Flash and receiving a direct image URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and reference images are sent to the external Agnes API for processing. <br>
Mitigation: Do not submit confidential, personal, regulated, or private images or prompts unless the user accepts the external processing behavior. <br>
Risk: Generated images are returned as direct public cloud-hosted URLs. <br>
Mitigation: Treat output URLs as publicly accessible and avoid generating content that should remain private. <br>
Risk: The skill requires an Agnes API key for authenticated requests. <br>
Mitigation: Store the API key in an environment variable such as AGNES_API_KEY and avoid hardcoding credentials in scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lg0219/skills/agnes-image-generator) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON success or error objects, plus Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Successful image operations return direct public cloud-hosted image URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
