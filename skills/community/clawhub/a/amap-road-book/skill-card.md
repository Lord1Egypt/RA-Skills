## Description: <br>
Generates Amap travel roadbooks from natural-language trip requests, including clarification questions, place resolution, route planning, daily timelines, weather reminders, and HTML, JSON, and Excel outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuo-wentao](https://clawhub.ai/user/zuo-wentao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travel planners and ClawHub/OpenClaw users use this skill to turn natural-language itinerary ideas into executable Amap roadbooks with map-ready route data, shareable HTML pages, and Excel planning sheets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default public publishing can expose itinerary details such as dates, lodging areas, companions, and budget. <br>
Mitigation: Use local-only mode when privacy matters, avoid adding sensitive personal details, and share public links only with trusted recipients. <br>
Risk: Amap credentials may be exposed if they are included in generated or published outputs. <br>
Mitigation: Use restricted or throwaway Amap keys for this skill and rotate any credentials that were already used in published outputs. <br>
Risk: Generated travel details can depend on third-party data and may omit or misstate prices, schedules, availability, or opening hours. <br>
Mitigation: Confirm tickets, schedules, prices, lodging, and time-sensitive travel details with authoritative sources before relying on the itinerary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zuo-wentao/amap-road-book) <br>
- [Publisher profile](https://clawhub.ai/user/zuo-wentao) <br>
- [Amap Open Platform](https://lbs.amap.com/) <br>
- [Amap API map](references/amap-api-map.md) <br>
- [Clarification policy](references/clarification-policy.md) <br>
- [Roadbook schema](references/roadbook-schema.md) <br>
- [Demo scenarios](references/demo-scenarios.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown responses with route summaries, assumptions, links or file paths, map-renderable JSON, HTML output, and Excel workbook output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provided Amap Web Service, JavaScript API, and JavaScript security credentials; public publishing is enabled by default unless local-only output is requested.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
