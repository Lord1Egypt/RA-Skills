## Description: <br>
A dive trip planning assistant that gathers travel dates, budget, certification level, destination and marine-life preferences, then searches flyai for flights, hotels, dive shops and booking links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rayzougit](https://clawhub.ai/user/rayzougit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan dive trips through a guided conversation, compare itinerary options across budget tiers, and review flight, hotel and dive-shop recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for travel preferences and uses flyai for travel search, so users may share trip details with an external service. <br>
Mitigation: Share only information needed for planning and avoid sensitive identity, passport or payment details in the planning conversation. <br>
Risk: Generated flight, hotel and dive-shop links point to external booking sites and may vary in accuracy, availability or trustworthiness. <br>
Mitigation: Verify each destination, operator reputation, booking URL and final price before paying or relying on the itinerary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rayzougit/dive-trip-planner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with conversational prompts, comparison tables, itinerary details and booking links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces multi-budget recommendations and Top 10 flight and hotel lists when enough travel details are available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
