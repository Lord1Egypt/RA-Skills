## Description: <br>
抖音全网实时热点 helps content creators, operators, e-commerce teams, and marketers retrieve current Douyin hotlist topics and rising discussion signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allinherog-star](https://clawhub.ai/user/allinherog-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, operations teams, e-commerce teams, and marketers use this skill to check current Douyin hotlist entries and identify timely topics for daily trend scans, content planning, and follow-up analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a sensitive API key and sends requests to ai-skills.ai. <br>
Mitigation: Provide only the required AI Skills API key through environment variables and avoid sharing it in prompts or parameters. <br>
Risk: Business context sent in parameters could be exposed to an external service. <br>
Mitigation: Avoid confidential business context and review parameters before invocation. <br>
Risk: Implicit invocation may call the external service unexpectedly in permissive agent environments. <br>
Mitigation: Narrow or disable implicit invocation where supported. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/allinherog-star/douyin-hotlist-overall) <br>
- [AI Skills](https://ai-skills.ai) <br>
- [Douyin hot search endpoint](https://www.douyin.com/aweme/v1/web/hot/search/list/) <br>
- [Skill configuration](references/skill.json) <br>
- [Input schema](references/form-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [JSON data, text, guidance] <br>
**Output Format:** [JSON response with hotlist entries, timestamps, ranking positions, heat values, and execution metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISKILLS_API_KEY and calls ai-skills.ai for Douyin hotlist results.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
