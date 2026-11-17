## Description:

自由行旅游出行管家的统一入口，负责意图识别、路由分发和跨技能协调，面向老年旅行者处理行程查询、身体不适、迷路、评价服务和旅行照片等请求。

This skill is ready for commercial/non-commercial use.

## Publisher:

[suying1023](https://clawhub.ai/user/suying1023)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel service teams use this skill as an elder-friendly travel assistant that routes requests across itinerary lookup, proactive trip support, reviews, and travel video generation. It is designed for parents or older travelers who need voice-first help with travel logistics, safety issues, and service coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad automatic authority over emergency, health, location, review, and media-sharing workflows may cause unintended actions.

Mitigation: Require explicit opt-in for health, GPS, wearable, call, media, biometric, and social-sharing features, with human confirmation where feasible.

Risk: Emergency workflows can affect personal safety and may be abused if unauthenticated or triggered too freely.

Mitigation: Use authenticated, auditable, and rate-limited emergency workflows with clear escalation rules and manual override paths.

Risk: Health, location, biometric, and contact data are sensitive and may be disclosed to third parties during travel support.

Mitigation: Document third-party disclosures, minimize shared data, encrypt health records, and require consent before sharing sensitive information.

Risk: Medication guidance in travel-emergency dialogues may create clinical risk.

Mitigation: Remove medication instructions or require clinical review before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/suying1023/skills/flyai-elder-travel-care-core)
- [Core skill definition](artifact/SKILL.md)
- [Skill architecture overview](artifact/README.md)
- [Emergency and health profile API](artifact/tools/tool-api-reference-emergency.md)
- [Elder travel data models](artifact/tools/tool-data-models-v3.md)
- [General API reference](artifact/tools/tool-api-reference.md)
- [Fliggy order API documentation](https://yuque.antfin.com/fliggy/order-api)
- [Alibaba Cloud intelligent voice interaction](https://help.aliyun.com/product/30463.html)
- [DingTalk open platform documentation](https://open.dingtalk.com/document/)
- [Alibaba Cloud video service](https://help.aliyun.com/product/29939.html)
- [China Ministry of Culture and Tourism](https://www.mct.gov.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration Guidance]

**Output Format:** [Markdown or plain text with structured routing decisions and API-oriented examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include itinerary details, emergency escalation prompts, review summaries, video-sharing guidance, and configuration values.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
