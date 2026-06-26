## Description: <br>
Helps parents plan family travel by searching child-friendly hotels and packages, comparing playground quality and supervision needs, and producing age- and preference-aware itinerary guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dutxueyu](https://clawhub.ai/user/dutxueyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents and travel-planning agents use this skill to compare child-friendly hotels, packages, and nearby activities for weekend or holiday trips. It is especially focused on matching venues to a child's age and preferences while highlighting whether adult supervision is required. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send destination, dates, preferences, and child-related planning details to FlyAI/Fliggy-backed searches. <br>
Mitigation: Share only the minimum details needed for planning, prefer interest-based preferences over child gender when possible, and review the FlyAI CLI and travel account used for searches. <br>
Risk: Hotel playground fees, supervision rules, and travel prices can be incomplete or change after search results are returned. <br>
Mitigation: Verify booking details on the provider page and call the hotel or venue when supervision requirements or child-safety assumptions affect the plan. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dutxueyu/easytravelwithchild) <br>
- [Parent-child hotel rating standards](references/hotel-rating-standards.md) <br>
- [Child venue classification guide](references/venue-classification.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with comparison tables, itinerary sections, booking links, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses real-time FlyAI/Fliggy-backed search results; prices, availability, fees, and supervision requirements should be verified before booking.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
