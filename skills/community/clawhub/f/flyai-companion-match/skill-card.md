## Description: <br>
同行人适配推荐助手，根据同行人特征（老人、小孩、闺蜜等）智能筛选目的地景点。调用FlyAI获取景点数据，结合同行人画像自动过滤，推荐适合所有同行人的景点和玩法。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to collect destination and companion details, search FlyAI travel data, and recommend attractions and nearby lodging that fit children, older adults, families, friends, or other travel groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to install or upgrade the FlyAI CLI globally before travel searches. <br>
Mitigation: Review the CLI requirement first, avoid sudo installs for routine use, and only install from a trusted package source in an environment where global npm changes are acceptable. <br>
Risk: The skill suggests bypassing TLS verification with NODE_TLS_REJECT_UNAUTHORIZED=0 when SSL certificate validation fails. <br>
Mitigation: Do not use TLS bypasses for routine searches; resolve certificate or network issues instead. <br>
Risk: The skill may read or save personalization data through memory or ~/.flyai/user-profile.md. <br>
Mitigation: Confirm what profile data is being reused or stored, and only save preferences after user approval. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/hello-ahang/flyai-companion-match) <br>
- [FlyAI tool reference](artifact/reference/tools.md) <br>
- [User profile storage](artifact/reference/user-profile-storage.md) <br>
- [Attraction search](artifact/reference/search-poi.md) <br>
- [Hotel search](artifact/reference/search-hotel.md) <br>
- [Keyword search](artifact/reference/keyword-search.md) <br>
- [AI search](artifact/reference/ai-search.md) <br>
- [Flight search](artifact/reference/search-flight.md) <br>
- [Train search](artifact/reference/search-train.md) <br>
- [Examples](artifact/reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown travel recommendations with inline shell commands and structured attraction scoring] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include attraction rankings, itinerary suggestions, hotel-search prompts, and profile-save prompts.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
