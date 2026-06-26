## Description: <br>
Provides a daily WeChat writing workflow that pitches topics, supports article drafting, and uploads prepared drafts with images to WeChat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robertstarry-gif](https://clawhub.ai/user/robertstarry-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and operators use this skill to generate daily Chinese WeChat topic pitches, prepare concise human-interest or AI-focused articles, and move reviewed markdown content into WeChat drafts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive WeChat credentials and can use them to create drafts. <br>
Mitigation: Use test WeChat credentials first, keep credentials scoped and private, and connect a production account only after confirming the workflow. <br>
Risk: Markdown with untrusted remote image URLs may cause the uploader to fetch arbitrary image URLs. <br>
Mitigation: Use trusted image sources only and add URL-fetch safeguards or explicit upload confirmation before processing third-party content. <br>
Risk: The automation may overstate which parts are real versus mock behavior. <br>
Mitigation: Run the scripts manually in a staging workflow and verify each pitch, image, and draft before relying on scheduled automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robertstarry-gif/daily-wechat-writer) <br>
- [Publisher profile](https://clawhub.ai/user/robertstarry-gif) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create WeChat draft uploads when configured with WeChat credentials and image inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
