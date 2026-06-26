## Description: <br>
工程化备课系统（Course-Prep-Auto-Flow v1.0）将课程主题、受众画像和参考素材转化为七步备课流程，覆盖信息采集、骨架设计、素材提炼、内容填充、结构审查、配图规划和终局产出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yipng05-max](https://clawhub.ai/user/yipng05-max) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
课程设计者、培训讲师和内容创作者使用该技能，将课程主题、受众画像和参考素材逐步整理为公开课、直播课或工作坊的备课稿、复盘文档和配图规划。 <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Course prompts, reference materials, generated images, and final drafts may be sent to the configured image provider and Feishu workspace. <br>
Mitigation: Use only approved services for the data involved, avoid confidential or regulated course material unless approved, and review generated drafts before sharing. <br>
Risk: The workflow references a custom image API endpoint, an image-generation helper skill, and a Google API key. <br>
Mitigation: Verify the endpoint and helper skill before use, store credentials securely, and use limited-scope credentials where possible. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yipng05-max/course-prep-afp) <br>
- [详细说明文档](https://www.feishu.cn/docx/GmQUdwj4sosWxvxQp84cIf8NnQb) <br>
- [Configured image API endpoint](https://work.poloapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces staged course-preparation drafts, image prompts, document URLs, and review checkpoints that require user confirmation between phases.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
