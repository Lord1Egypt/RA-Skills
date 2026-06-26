## Description: <br>
本技能通过调用灵伴智能的AI影视工场（DramaAIStudio）平台的多项能力，辅助AI短剧创作者更方便地参与创作，具体包括：项目的创建与管理，剧本的上传与自动分析，资产（角色、场景、道具）的智能提取与图像生成，分镜脚本生成与管理、分镜视频生成等。本技能还支持创建项目的定时巡检任务，将项目的关键节点完成情况即时地通知给创作者，完成生成、查看、评论、反馈和优化的创作闭环。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hobinson](https://clawhub.ai/user/hobinson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and production teams use this skill to operate DramaAIStudio workflows from an agent, including short-drama project setup, script upload and analysis, asset extraction and generation, storyboard management, video generation, and review feedback. The skill can also create scheduled monitoring tasks for project asset and storyboard-video changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an iDrama API token and can store credentials or state locally. <br>
Mitigation: Prefer host-managed secrets, avoid persisting tokens in .env unless explicitly needed, and restrict any stored token file to the current user. <br>
Risk: Recurring monitoring jobs can repeatedly access project media and report returned image or video URLs. <br>
Mitigation: Enable scheduled monitoring only for needed projects, review scheduled jobs regularly, and treat media URLs as sensitive links. <br>
Risk: Persistent agent rules and local state can influence later agent behavior. <br>
Mitigation: Review the installed rules and session_state.json before use, especially when switching projects or sharing an environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hobinson/drama-ai-studio) <br>
- [Publisher profile](https://clawhub.ai/user/hobinson) <br>
- [iDrama API token page](https://idrama.lingban.cn/api-token) <br>
- [iDrama API base URL](https://idrama.lingban.cn/) <br>
- [Drama project APIs](artifact/references/ref-4-1-get-openapi-drama-list.md) <br>
- [Script upload and analysis APIs](artifact/references/ref-5-2-post-openapi-drama-play-id-scripts-upload.md) <br>
- [Asset image generation API](artifact/references/ref-6-6-post-openapi-drama-play-id-assets-asset-type-asset-id-generate-image.md) <br>
- [Storyboard prompt optimization API](artifact/references/ref-7-5-post-openapi-drama-play-id-storyboard-episode-no-shots-shot-id-optimize-prompt.md) <br>
- [Storyboard video generation task API](artifact/references/ref-8-1-post-openapi-drama-play-id-storyboard-video-episodes-episode-no-shots-shot-id-tasks.md) <br>
- [Server-resolved provenance](unavailable: No server-resolved GitHub import provenance is stored for this version.) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown guidance with HTTP request details, JSON examples, shell commands, and Python script invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IDRAMA_TOKEN for authenticated iDrama API access; may update local project state and scheduled monitoring snapshots.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
