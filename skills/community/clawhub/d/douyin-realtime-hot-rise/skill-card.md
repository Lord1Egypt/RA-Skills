## Description: <br>
抖音上升热点选题助手适合内容创作者、运营、电商、营销在用户想知道接下来拍什么、写什么更可能有流量时使用，帮助基于输入材料生成上升热点列表、排名和变化趋势视图、可用于内容规划的选题线索。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External content creators, operations teams, e-commerce teams, and marketers use this skill to identify rising Douyin topics, ranking changes, and trend signals for content planning. It is intended for topic selection, short-video planning, campaign observation, and timely response to fast-moving trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runner sends Douyin trend keywords, tags, ordering choices, and related request metadata to ai-skills.ai. <br>
Mitigation: Avoid entering secrets, confidential business plans, or sensitive personal data in query parameters, and review requested inputs before execution. <br>
Risk: The skill requires AISKILLS_API_KEY, a sensitive credential used for API authentication. <br>
Mitigation: Store the API key outside prompts and source files, pass it through the environment, and rotate it if it is exposed. <br>
Risk: Trend data may be time-sensitive and can become stale quickly. <br>
Mitigation: Use results as planning signals and verify important trend decisions against current Douyin context before publishing or investing. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/allinherog-star/douyin-realtime-hot-rise) <br>
- [Publisher Profile](https://clawhub.ai/user/allinherog-star) <br>
- [form-schema.json](references/form-schema.json) <br>
- [skill.json](references/skill.json) <br>
- [AI Skills](https://ai-skills.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples and command-line invocation details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runtime responses are JSON from the AI Skills API, including success status, trend data, pagination, and execution metadata.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
