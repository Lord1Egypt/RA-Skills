## Description: <br>
Generate images with Doubao web chat, extract the final generated image URL from the page, save the image locally, and return the saved local path. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Likely7](https://clawhub.ai/user/Likely7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to operate Doubao web chat for browser-based image generation, save the selected generated image locally, and return the saved path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and browser session state may be sent to Doubao during image generation. <br>
Mitigation: Avoid sensitive prompts unless the user is comfortable sending them to Doubao, and make clear that the workflow may use an already logged-in browser session. <br>
Risk: An unintended local path could overwrite or place generated image files somewhere unexpected. <br>
Mitigation: Use a deliberate output path when possible and confirm the saved file path before relying on the result. <br>


## Reference(s): <br>
- [Doubao web chat](https://www.doubao.com/chat/) <br>
- [ClawHub skill page](https://clawhub.ai/Likely7/doubaoimages) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with local file path and optional source image URL] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill saves a generated image to local disk and returns the final local save path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
