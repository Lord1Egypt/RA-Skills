## Description:

橙星梦工厂AI视频制作工具，通过对话式操作，用户可以创建项目、配置剧本、生成角色/分镜/视频、查询任务状态。

This skill is ready for commercial/non-commercial use.

## Publisher:

[amireux0013](https://clawhub.ai/user/amireux0013)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate the FunAI comic-video workflow through an agent, including project creation, script submission, character and storyboard generation, task polling, and final video composition.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags mutable remote update metadata as a risk before task-creating operations.

Mitigation: Review and trust the remote setup endpoint before installing or updating, and prefer disabling automatic skill updates in controlled environments.

Risk: The release evidence flags local FunAI token handling as unsafe.

Mitigation: Keep the token out of project files, restrict permissions on local config files, and rotate the token if exposure is suspected.

Risk: Raw absolute-URL API calls can expose users to unintended endpoints or brittle behavior.

Mitigation: Review API targets before execution and avoid raw absolute-URL calls unless the endpoint is expected and trusted.

## Reference(s):

- [Funai-skill on ClawHub](https://clawhub.ai/amireux0013/skills/funai-skill)
- [FunAI Token Page](https://ai.fun.tv/#/openclaw)
- [FunAI Project Page Template](https://ai.fun.tv/#/comic/multiple?projectId={projectId})
- [Remote Skill Setup Metadata](https://neirong.funshion.net/skills/setup-skill.md)
- [Project Management API](references/01-project-management.md)
- [Script Management and Workflow API](references/02-script-management.md)
- [Character Management API](references/03-character-management.md)
- [Voice Management API](references/04-voice-management.md)
- [Storyboard Management API](references/05-storyboard-management.md)
- [Video Generation and Composition API](references/06-video-generation.md)
- [Task Status API](references/07-task-status.md)
- [Resource Management API](references/08-resources.md)
- [Error Codes](references/09-error-codes.md)
- [Models and Configuration](references/10-models-and-config.md)
- [Best Practices](references/11-best-practices.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing workflow guidance, API request examples, local configuration steps, and shell commands for interacting with FunAI.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
