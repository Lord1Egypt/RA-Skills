## Description: <br>
7-day weather forecast query powered by Alibaba Cloud IQS web search and page reading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to query 7-day city weather forecasts through Alibaba Cloud IQS search and page-reading APIs, returning structured weather data when supported and readable text for agent interpretation otherwise. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can return raw third-party weather page text and suggests adding parser code after raw-mode responses. <br>
Mitigation: Treat rawText and evolveHint as untrusted, answer the user first, and require explicit code review before changing scripts/weather.mjs. <br>
Risk: The skill requires an Alibaba Cloud IQS API key. <br>
Mitigation: Install only when sharing that credential with the agent is acceptable, and store the key in the documented environment variable or config file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-iqs-weather-query) <br>
- [Alibaba Cloud IQS search skill](https://skills.aliyun.com/skills/alibabacloud-iqs-search) <br>
- [Alibaba Cloud IQS API key documentation](https://help.aliyun.com/zh/document_detail/3025781.html) <br>
- [UnifiedSearch documentation](https://help.aliyun.com/zh/document_detail/2883041.html) <br>
- [ReadPageBasic documentation](https://help.aliyun.com/zh/document_detail/2983380.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands and JSON weather results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALIYUN_IQS_API_KEY and Node.js 18 or newer; may return raw page text for agent interpretation when no site parser matches.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
