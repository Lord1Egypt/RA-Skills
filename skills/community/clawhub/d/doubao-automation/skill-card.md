## Description: <br>
豆包自动化操作 lets an agent control a logged-in Microsoft Edge browser through Playwright CDP to use Doubao for chat, image and video generation, batch generation, and downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hitjcl](https://clawhub.ai/user/hitjcl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users who already use Doubao in Edge can ask an agent to run Doubao chats, create or download generated images and videos, and process prompt lists in batches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls a logged-in Edge browser through CDP and can disrupt or expose normal browsing sessions. <br>
Mitigation: Use a separate Edge profile with only Doubao logged in, and close sensitive tabs before running the skill. <br>
Risk: The startup flow can close existing Edge windows before relaunching Edge in CDP mode. <br>
Mitigation: Save browser work first, or run the skill from a dedicated browser profile that is not used for normal browsing. <br>
Risk: Image-to-video operations can send the selected local image file to Doubao. <br>
Mitigation: Review the image path and file contents before running image-to-video, and avoid sending sensitive files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hitjcl/doubao-automation) <br>
- [Doubao](https://www.doubao.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands, console text, JSON result summaries, and downloaded media files when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a logged-in Edge browser session reachable through localhost CDP; generated media downloads are saved to the requested output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
