## Description: <br>
抖音账号诊断宗师 accepts a Douyin account name or ID, queries RedFox account and content data, and produces a four-dimension account diagnosis covering account scale, content performance, operational activity, and platform index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[if530770](https://clawhub.ai/user/if530770) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External brands, MCN operators, creators, and content operations teams use this skill to evaluate Douyin account quality, compare account performance, and generate data-backed optimization suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a RedFox API key and sends entered Douyin account names or IDs to RedFox for lookup. <br>
Mitigation: Configure the key only in the expected environment variable, avoid exposing it in prompts or logs, and use the skill only when sending those account identifiers to RedFox is acceptable. <br>
Risk: API calls may consume RedFox credits. <br>
Mitigation: Use explicit account lookup requests and confirm that API-credit consumption is acceptable before repeated or batch-style use. <br>
Risk: Fallback results from non-RedFox sources may be lower confidence. <br>
Mitigation: Prefer RedFox-backed results and clearly treat fallback data as lower confidence when RedFox lookup is unavailable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/if530770/douyin-account-diagnosis) <br>
- [Core workflow](references/core_workflow.md) <br>
- [RedFox API endpoint](https://redfox.hk/story/api/dyUser/query) <br>
- [Publisher profile](https://clawhub.ai/user/if530770) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown diagnostic report with scoring breakdowns, account metrics, risk notes, and optimization guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; account names or IDs entered by the user are sent to RedFox for lookup and may consume API credits.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
