## Description: <br>
Unified elder-travel assistant entry skill for intent recognition, skill routing, emergency prioritization, and cross-skill coordination across itinerary, companion, review, and travel-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[suying1023](https://clawhub.ai/user/suying1023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers, family coordinators, and service teams use this skill to help older adults query travel plans, request trip support, submit service feedback, and receive safety-focused escalation during independent travel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may coordinate emergency dispatch, health records, and live location in sensitive travel scenarios. <br>
Mitigation: Require explicit traveler opt-in, strong identity checks, bounded permissions, audit logs, retention limits, and human escalation for emergency or health-related actions. <br>
Risk: The skill may post media, change bookings, submit reviews, or contact third parties on a traveler's behalf. <br>
Mitigation: Require hard confirmation before each high-impact action and keep a clear cancellation or human-support path. <br>
Risk: Delegated authority across family members, service providers, and platform support can create weak consent boundaries. <br>
Mitigation: Limit actions to pre-approved contacts and services, verify the traveler or authorized coordinator before sharing data, and log all third-party interactions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/suying1023/flyai-elder-travel-care-core) <br>
- [Core skill instructions](artifact/SKILL.md) <br>
- [Skill architecture overview](artifact/README.md) <br>
- [Emergency API reference](artifact/tools/tool-api-reference-emergency.md) <br>
- [API reference](artifact/tools/tool-api-reference.md) <br>
- [Data models v3](artifact/tools/tool-data-models-v3.md) <br>
- [Edge cases and safety flows](artifact/examples/edge-cases.md) <br>
- [Aliyun Intelligent Speech Interaction](https://help.aliyun.com/product/30463.html) <br>
- [DingTalk Open Platform documentation](https://open.dingtalk.com/document/) <br>
- [Aliyun Video on Demand](https://help.aliyun.com/product/29939.html) <br>
- [China Ministry of Culture and Tourism](https://www.mct.gov.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, API Calls] <br>
**Output Format:** [Markdown and text responses with structured routing, escalation, service-coordination, and media-generation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include itinerary summaries, emergency escalation prompts, review drafts, and media-sharing instructions; high-impact actions require explicit confirmation and human escalation paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
