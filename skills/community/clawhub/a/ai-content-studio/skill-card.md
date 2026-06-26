## Description: <br>
AI全链路内容工坊 — 多平台内容一键创作与发布自动化工作流，涵盖选题研究、文章撰写、知识卡片生成、全平台发布。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, brand operators, personal IP builders, and enterprise marketing teams use this skill to research topics, draft long-form WeChat articles, generate knowledge-card assets, adapt Xiaohongshu copy, and coordinate multi-platform publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish to real WeChat and Xiaohongshu accounts without a clearly enforced approval step. <br>
Mitigation: Configure draft or preview output by default, keep credentials in a secure secret store with minimal scopes, and require explicit human confirmation before each platform post. <br>
Risk: The workflow depends on multiple content, rendering, and publishing skills, so downstream behavior can affect the safety of the overall release. <br>
Mitigation: Install only trusted dependent skills and review generated articles, captions, images, and scheduled publishing settings before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zlszhonglongshen/ai-content-studio) <br>
- [RSSHub 36Kr feed](https://rsshub.app/36kr/posts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with workflow steps, inline shell commands, generated article text, captions, and file references for image cards] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce public-posting actions through dependent publishing skills when configured with platform credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
