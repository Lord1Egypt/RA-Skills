## Description: <br>
零配置即装即用，覆盖潜水全链路服务——潜点搜索、考证指南、安全检查，以及机票酒店交通美食预订，国内走飞猪高德国际走RG自动分流，所有预订链路支持分佣。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[travel-skills](https://clawhub.ai/user/travel-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Divers and travel planners use this skill to compare dive sites, review certification and safety guidance, and search flights, hotels, transport, and restaurants for dive trips. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Travel searches may send dates, origins, destinations, hotel searches, and location or food queries through SCF proxy services. <br>
Mitigation: Use the skill only when comfortable sharing those search details, and avoid entering sensitive personal information beyond what is needed for search. <br>
Risk: Prices and booking links are third-party search results and may change. <br>
Mitigation: Confirm price, availability, booking terms, and provider details on the destination booking page before purchasing. <br>
Risk: Dive safety and certification information is informational and cannot replace professional instruction, medical advice, or local emergency response. <br>
Mitigation: Treat safety guidance as a planning aid, follow certified instructor and local operator requirements, and seek qualified medical or emergency help when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/travel-skills/dive-travel-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON strings with travel, booking, and dive guidance fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include third-party booking URLs, prices, route details, restaurant results, dive site attributes, certification notes, and safety reminders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
