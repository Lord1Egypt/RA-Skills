## Description: <br>
Plans WeChat sticker, nine-grid, and multi-image posts, guiding an agent from topic and visual sequence design through AI image generation and optional WeChat publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiworkskills](https://clawhub.ai/user/aiworkskills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External WeChat operators, self-media teams, and IP account owners use this skill to create image-first public-account posts with a consistent theme, ordered image plan, review checklist, and optional publish path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires sensitive image-model and WeChat credentials. <br>
Mitigation: Protect aws.env, install only when the aiworkskills WeChat publishing suite is intended, and verify companion image and publish skills before using credentials. <br>
Risk: Image prompts and generated image files may be sent to external image-model and WeChat APIs. <br>
Mitigation: Review generated images, draft settings, and upload targets before allowing any upload or WeChat publication. <br>
Risk: Publishing can affect a live WeChat account when the publish path is used. <br>
Mitigation: Require explicit user confirmation before uploading materials or publishing drafts to WeChat. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aiworkskills/aws-wechat-sticker) <br>
- [Publisher profile](https://clawhub.ai/user/aiworkskills) <br>
- [贴图图序规划](references/workflow.md) <br>
- [贴图审稿清单](references/checklist.md) <br>
- [AIWorkSkills homepage](https://aiworkskills.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated workflow files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces image outlines, prompt files, generated image assets, and review or publish guidance for a single WeChat post workflow.] <br>

## Skill Version(s): <br>
1.0.23 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
