## Description: <br>
使用 FlyAI 进行高铁票和飞机票比价，给用户推荐最优出行方式，并支持弃程票搜索和前后一天价格对比。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jixinda](https://clawhub.ai/user/jixinda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers and travel-planning agents use this skill to compare Chinese high-speed rail and flight options by price, estimated total travel time, comfort, convenience, and adjacent-day fare differences. It may also surface hidden-city ticket options when cheaper, with risk warnings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags the skill as suspicious because it operationalizes hidden-city or throwaway-ticket suggestions during ordinary travel planning. <br>
Mitigation: Review before installing and use only when hidden-city ticket advice is intentionally desired; otherwise prefer standard rail and flight comparison behavior. <br>
Risk: Hidden-city ticket recommendations can create travel risks such as checked-baggage problems, cancelled onward or return segments, frequent-flyer consequences, flight-change routing issues, and airline contract violations. <br>
Mitigation: Require clear user-facing warnings before presenting those options and limit any recommendation to cases where the user understands the constraints, such as one-way travel without checked baggage. <br>
Risk: FlyAI searches may send route, date, and preference details to an external service. <br>
Mitigation: Avoid sharing unnecessary personal details and make the external-search dependency clear before using it with sensitive itineraries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jixinda/flyai-price-compare) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown travel comparison with tables, recommendations, risk notes, and optional FlyAI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on real-time rail and flight availability, user route, date, and travel constraints.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
