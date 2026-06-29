## Description: <br>
全能旅行规划师根据出发地、目的地、预算、天数、人数和偏好生成覆盖交通、住宿、餐饮、景点、预算和备选方案的旅行计划。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nameused](https://clawhub.ai/user/nameused) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to produce structured travel plans for domestic or international destinations, including itinerary timing, transport choices, food and lodging suggestions, budget allocation, weather preparation, and contingency options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated itinerary files may be saved in the workspace and could contain sensitive travel details. <br>
Mitigation: Confirm the save location before generating files and avoid including passport, payment, private contact, or sensitive booking details unless local storage is acceptable. <br>
Risk: Travel, fare, weather, restaurant, lodging, and attraction details can change after a plan is generated. <br>
Mitigation: Verify time-sensitive bookings, prices, hours, restrictions, and transportation details with current sources before purchase or departure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nameused/skills/all-round-travel-planner) <br>
- [Destination templates and transport query guide](references/destination_templates.md) <br>
- [HTML travel-plan output template](references/html_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown by default, with optional single-file HTML, tables, documents, presentations, or visual itinerary artifacts when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use current web research for destination, transport, fare, weather, restaurant, lodging, and attraction details; generated trip documents may be saved locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
