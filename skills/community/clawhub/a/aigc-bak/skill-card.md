## Description: <br>
Aigc.Bak helps agents generate AI images from text prompts with negative prompts, aspect ratio selection, batch generation, and Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gushenjie](https://clawhub.ai/user/gushenjie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to trigger text-to-image generation from chat requests, tune negative prompts, aspect ratios, and batch size, and deliver generated images through OSS and Feishu workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use bundled or environment credentials when uploading generated images. <br>
Mitigation: Remove and rotate the bundled OSS token, and require each user to provide a scoped credential before installation or execution. <br>
Risk: Generated images can be uploaded to OSS and forwarded to Feishu, which may expose private prompts or images. <br>
Mitigation: Make OSS upload and Feishu forwarding explicit opt-in actions, and verify the destination before using the skill with private content. <br>
Risk: The Feishu sender component is referenced as an external local dependency. <br>
Mitigation: Verify or package the Feishu sender component before deployment so users know which code handles image delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gushenjie/aigc-bak) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, configuration] <br>
**Output Format:** [Plain text status messages with generated image URLs or Feishu send results; image files may be downloaded and forwarded by the script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports prompt, negative prompt, aspect ratio, batch size, and timeout options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
