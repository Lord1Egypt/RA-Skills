## Description: <br>
Generate images from text prompts via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarjorieBroad](https://clawhub.ai/user/MarjorieBroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other ClawHub users use this skill to generate an image URL from a text prompt through an external image generation API, with an optional shell step to save the image file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and API keys are sent to an external image generation provider. <br>
Mitigation: Avoid sensitive prompts, use a dedicated or limited API key where possible, and install only if that external data sharing is acceptable. <br>
Risk: The API key is passed to the generator command as an argument. <br>
Mitigation: Prefer safer secret handling where possible and avoid exposing credentials in shell history, logs, or shared process listings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/MarjorieBroad/ai-imggen) <br>
- [SkillBoss](https://www.skillboss.co) <br>
- [HeyBoss image API endpoint](https://api.heybossai.com/v1/run) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text image URL or JSON from a Node.js command, with an optional saved image file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and SKILLBOSS_API_KEY.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
