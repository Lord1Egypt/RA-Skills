## Description: <br>
An intelligent trip-planning skill that uses flight, hotel, and attraction data to generate complete travel itineraries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yunhanli7](https://clawhub.ai/user/yunhanli7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to plan leisure, family, business-plus-leisure, food-focused, or parent-child trips by requesting a destination, duration, budget, and preferences. The skill produces a complete itinerary covering transportation, lodging, attractions, restaurants, practical tips, and a budget estimate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A normal travel-planning request can trigger a global npm install of `@fly-ai/flyai-cli`. <br>
Mitigation: Preinstall a trusted, pinned version in a managed or sandboxed environment and require explicit approval before setup commands run. <br>
Risk: Travel recommendations, prices, schedules, availability, images, and booking links depend on external real-time data. <br>
Mitigation: Review generated itineraries and verify booking details before purchase or travel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yunhanli7/fliggy-trip-planner) <br>
- [Publisher profile](https://clawhub.ai/user/yunhanli7) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tables, images, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes itinerary overview, flight and hotel comparisons, daily schedule, practical tips, and budget table.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
