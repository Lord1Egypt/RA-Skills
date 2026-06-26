## Description: <br>
一体化健身追踪系统。自动同步饮食记录和身体状态到 intervals.icu。支持配置引导和错误处理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leozvc](https://clawhub.ai/user/leozvc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to record meals, estimate nutrition, review training and recovery status, and sync wellness data with their own Intervals.icu account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores an Intervals.icu API key and can read sensitive fitness and wellness data. <br>
Mitigation: Use a dedicated revocable API key, keep the local config file private, and revoke or rotate the key if the file may have been exposed. <br>
Risk: Natural-language meal prompts can update wellness records in Intervals.icu. <br>
Mitigation: Use dry-run mode before syncing meals and prefer explicit commands over broad group-chat triggers. <br>
Risk: Food names may be sent to OpenFoodFacts for nutrition lookup. <br>
Mitigation: Use the no-OpenFoodFacts option when food names should not leave the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leozvc/fitness-personal-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/leozvc) <br>
- [Intervals.icu API Integration Cookbook](https://forum.intervals.icu/t/intervals-icu-api-integration-cookbook/80090) <br>
- [API access to Intervals.icu](https://forum.intervals.icu/t/api-access-to-intervals-icu/609) <br>
- [Intervals.icu API documentation](https://intervals.icu/api-docs.html) <br>
- [OpenFoodFacts API](https://wiki.openfoodfacts.org/Main_Page) <br>
- [Intervals.icu API docs summary](references/intervals_api_docs.md) <br>
- [Fitness planning principles](references/fitness_principles.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown and terminal output with Python command examples and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update Intervals.icu wellness records and may query OpenFoodFacts unless disabled.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
