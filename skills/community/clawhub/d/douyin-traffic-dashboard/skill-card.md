## Description: <br>
抖音流量分配大盘适合内容创作者、运营、电商、营销在用户想知道抖音流量正在流向哪些方向时使用，帮助基于输入材料生成流量分布、分类层级结构、可用于内容布局的平台方向信号。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operations teams, ecommerce teams, and marketers use this skill to inspect Douyin traffic distribution, category hierarchy, hot-count percentages, and platform direction signals for content planning and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runner sends requests with AISKILLS_API_KEY to ai-skills.ai by default, or to any configured AISKILLS_BASE_URL. <br>
Mitigation: Install and run only when that external request path is acceptable, keep the API key in environment variables, and review any custom base URL before execution. <br>
Risk: Implicit invocation could select the skill in unrelated conversations. <br>
Mitigation: Prefer explicit invocation for Douyin traffic analysis workflows and avoid enabling it broadly where unrelated prompts may trigger API calls. <br>
Risk: Traffic distribution outputs are platform direction signals and may be cached or time-sensitive. <br>
Mitigation: Use the returned update time and metadata when interpreting results, and avoid treating category percentages as a replacement for topic-level validation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/douyin-traffic-dashboard) <br>
- [Publisher profile](https://clawhub.ai/user/allinherog-star) <br>
- [AI Skills API service](https://ai-skills.ai) <br>
- [references/skill.json](references/skill.json) <br>
- [references/form-schema.json](references/form-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON API responses and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISKILLS_API_KEY and sends execution requests to ai-skills.ai by default, or to a configured AISKILLS_BASE_URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
