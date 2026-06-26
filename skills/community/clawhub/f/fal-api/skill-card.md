## Description: <br>
Fal.ai API generates images, videos, and audio through the fal.ai API, including FLUX, SDXL, Whisper, and other supported models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ricanwarfare](https://clawhub.ai/user/ricanwarfare) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to submit prompts, media URLs, and generation parameters to fal.ai models for image and video generation or audio transcription through agent workflows, a CLI, or a Python module. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, image URLs, audio URLs, and generation parameters are sent to fal.ai. <br>
Mitigation: Avoid secrets and regulated personal data in prompts or URLs, and use the skill only when sending that data to fal.ai is acceptable. <br>
Risk: API calls can consume paid fal.ai credits. <br>
Mitigation: Use a dedicated or limited FAL_KEY where possible and monitor fal.ai usage or billing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ricanwarfare/fal-api) <br>
- [fal.ai API key dashboard](https://fal.ai/dashboard/keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance, CLI output, Python return values, and URLs from fal.ai API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FAL_KEY; fal.ai API calls may consume paid credits.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
