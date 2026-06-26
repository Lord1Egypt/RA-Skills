## Description: <br>
橙星梦工厂AI视频制作工具，通过对话式操作，用户可以创建项目、配置剧本、生成角色/分镜/视频、查询任务状态。当用户要求使用橙星梦工厂平台、创建 AI 漫剧项目、或通过 API 与平台交互时使用。触发词：橙星梦工厂、ai.fun.tv、漫剧制作、AI漫剧、FunAI。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[amireux0013](https://clawhub.ai/user/amireux0013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate the FunAI video creation platform through an agent, including project creation, script submission, character and storyboard generation, scene video generation, task polling, rollback, and final video composition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to create, modify, roll back, and compose FunAI projects, which can change account state and consume platform credits. <br>
Mitigation: Use the skill only with a trusted publisher and account, require user confirmation before state-changing workflow steps, and review project actions before execution. <br>
Risk: The skill relies on an external setup and update endpoint before creation or modification actions. <br>
Mitigation: Require manual approval for updates and review the setup endpoint result before allowing the agent to install or update skill files. <br>
Risk: The local config/.env token functions as an account credential. <br>
Mitigation: Protect config/.env, avoid sharing logs or files containing AIFUN_TOKEN, and rotate the token if exposure is suspected. <br>
Risk: Automatic confirmation can bypass intended human review during testing or workflow execution. <br>
Mitigation: Avoid AUTO_CONFIRM outside deliberate testing and keep confirmation checkpoints for user-visible project, role, storyboard, and video-generation decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/amireux0013/funai-skill) <br>
- [Publisher profile](https://clawhub.ai/user/amireux0013) <br>
- [FunAI OpenClaw token setup](https://ai.fun.tv/#/openclaw) <br>
- [FunAI setup and update endpoint](https://neirong.funshion.net/skills/setup-skill.md) <br>
- [Project Management API](references/01-project-management.md) <br>
- [Script Management and Step Advancement API](references/02-script-management.md) <br>
- [Storyboard Management API](references/05-storyboard-management.md) <br>
- [Video Generation and Composition API](references/06-video-generation.md) <br>
- [Task Status Query API](references/07-task-status.md) <br>
- [Models and Configuration Reference](references/10-models-and-config.md) <br>
- [Best Practices Guide](references/11-best-practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON request examples, configuration values, and user-facing workflow summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent guidance for live FunAI workflow actions and may direct agents to create or modify platform projects through configured API credentials.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
