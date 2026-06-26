## Description: <br>
Generate or remix images using Gemini models with text prompts and multiple input images, supporting various styles, resolutions, and advanced model options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rdeangel](https://clawhub.ai/user/rdeangel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, creators, and other external users use this skill to generate new images, remix existing images, and compose multiple reference images through Gemini image models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected input images are sent to Google Gemini for processing. <br>
Mitigation: Use only prompts and images that are appropriate for the configured Gemini account and data-handling terms. <br>
Risk: A Gemini API key is required to run the skill. <br>
Mitigation: Keep GEMINI_API_KEY scoped, revocable, and out of shared logs or checked-in files. <br>


## Reference(s): <br>
- [Gemini Image Remix on ClawHub](https://clawhub.ai/rdeangel/gemini-image-remix) <br>
- [Publisher profile: rdeangel](https://clawhub.ai/user/rdeangel) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, Python 3.10 or newer, and a GEMINI_API_KEY; generated media is written as PNG files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
