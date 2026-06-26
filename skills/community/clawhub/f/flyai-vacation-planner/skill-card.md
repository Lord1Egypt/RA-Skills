## Description: <br>
智能拼假日历助手，帮助用户计算最优请假方案。输入目的地、可请假天数和出发城市，自动生成拼假方案并查询机票价格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan efficient vacation schedules by combining statutory holidays, weekends, and requested leave days, then compare travel windows with flight, hotel, destination, and visa information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs agents to install an unpinned global FlyAI CLI package. <br>
Mitigation: Install only from a trusted FlyAI CLI supply chain, prefer a pinned or sandboxed install, and avoid sudo unless the user explicitly accepts the risk. <br>
Risk: The skill can use persistent travel profile data such as home city, budget, family details, travel history, and special needs. <br>
Mitigation: Ask the user before saving profile details, and review or delete sensitive entries in memory or ~/.flyai/user-profile.md when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-vacation-planner) <br>
- [Publisher profile](https://clawhub.ai/user/hello-ahang) <br>
- [AI Search reference](reference/ai-search.md) <br>
- [Example conversations](reference/examples.md) <br>
- [China holiday reference](reference/holidays-cn.md) <br>
- [Keyword Search reference](reference/keyword-search.md) <br>
- [Flight Search reference](reference/search-flight.md) <br>
- [Hotel Search reference](reference/search-hotel.md) <br>
- [Marriott Hotel Search reference](reference/search-marriott-hotel.md) <br>
- [Marriott Package Search reference](reference/search-marriott-package.md) <br>
- [POI Search reference](reference/search-poi.md) <br>
- [Train Search reference](reference/search-train.md) <br>
- [User profile storage reference](reference/user-profile-storage.md) <br>
- [Visa rules reference](reference/visa-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with travel plan cards and inline FlyAI CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include flight price ranges, hotel or destination suggestions, visa reminders, and follow-up travel actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
