## Description: <br>
Doubao Media generates images from text, videos from text, and videos from image URLs using Doubao (Volcengine ARK). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[systiger](https://clawhub.ai/user/systiger) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to call Doubao/Volcengine ARK media models for text-to-image, text-to-video, and image-to-video generation from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and optional image URLs are sent to Volcengine ARK. <br>
Mitigation: Avoid sensitive prompts and private image URLs unless the deployment is approved for that data. <br>
Risk: The skill requires an ARK_API_KEY credential. <br>
Mitigation: Provide the key through the environment, do not hardcode it, and rotate it according to local credential policy. <br>
Risk: Generated media is written to the local output directory. <br>
Mitigation: Review generated files under ~/.openclaw/workspace/output before sharing or retaining them. <br>
Risk: The advertised auto-send behavior may not actually attach media to chat. <br>
Mitigation: Check the printed local file path and manually attach or inspect the saved media when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/systiger/doubao-media) <br>
- [Volcengine ARK documentation](https://www.volcengine.com/docs/82379) <br>
- [Volcengine ARK console and pricing](https://console.volcengine.com/ark) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media files are saved locally under ~/.openclaw/workspace/output when the script runs successfully.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
