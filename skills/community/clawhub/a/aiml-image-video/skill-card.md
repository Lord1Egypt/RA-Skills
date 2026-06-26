## Description: <br>
Generate images or videos via AIMLAPI from prompts, with retries, explicit User-Agent headers, and async video polling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aimlapihello](https://clawhub.ai/user/aimlapihello) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate image, image-to-image, text-to-video, and image-to-video media through AIMLAPI using prompt-driven helper scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected media are sent to AIMLAPI for remote generation. <br>
Mitigation: Do not include private, regulated, credential, or confidential content in prompts or media inputs unless AIMLAPI use is approved for that data. <br>
Risk: The image input option can upload any local file path it is given, not only image files. <br>
Mitigation: Pass only intended image files or trusted image URLs to image input options, and avoid credential files, SSH keys, browser profiles, and other sensitive paths. <br>


## Reference(s): <br>
- [AIMLAPI media notes](references/aimlapi-media.md) <br>
- [Image-to-Image (I2I) Generation](references/IMAGE-TO-IMAGE.md) <br>
- [Image-to-Video (I2V) Generation](references/IMAGE-TO-VIDEO.md) <br>
- [ClawHub skill page](https://clawhub.ai/aimlapihello/aiml-image-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and generated media files written by helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AIMLAPI_API_KEY; prompts, selected image inputs, and generation parameters are sent to AIMLAPI.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
