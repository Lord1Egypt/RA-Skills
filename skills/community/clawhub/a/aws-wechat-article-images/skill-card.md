## Description: <br>
Generates WeChat official-account cover images and article illustrations from article titles and content, selecting reusable visual styles and producing multiple image options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiworkskills](https://clawhub.ai/user/aiworkskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External editors, media teams, and brand designers use this skill to plan and generate WeChat article cover images and inline illustrations with reusable cover and article-image style presets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image prompts and possible article excerpts are sent to the configured image endpoint. <br>
Mitigation: Use a trusted image provider and review prompts before generation when articles contain sensitive business or customer information. <br>
Risk: The image API key is read from aws.env and sent as a bearer token to the configured endpoint. <br>
Mitigation: Use a dedicated low-privilege IMAGE_MODEL_API_KEY and keep unrelated secrets out of aws.env. <br>
Risk: A malicious or misconfigured image endpoint could return unsafe image download URLs. <br>
Mitigation: Keep the script's public HTTP/HTTPS-only download checks in place and verify image_model.base_url before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiworkskills/aws-wechat-article-images) <br>
- [Publisher profile](https://clawhub.ai/user/aiworkskills) <br>
- [AI Work Skills homepage](https://aiworkskills.cn) <br>
- [Cover style presets](references/cover-styles/README.md) <br>
- [Image style auto-selection](references/image-styles/auto-selection.md) <br>
- [Prompt construction guide](references/image-styles/prompt-construction.md) <br>
- [Image specifications](references/specs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, prompt files, image files, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and IMAGE_MODEL_API_KEY; may create or update article image prompts, generated images, and img_analysis.md.] <br>

## Skill Version(s): <br>
1.0.23 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
