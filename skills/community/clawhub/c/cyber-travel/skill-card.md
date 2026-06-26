## Description: <br>
Cyber Travel guides an agent through planning and writing immersive virtual travel itineraries, daily travelogues, image records, and optional share-ready PDFs based on real destination information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Travelers, writers, and agent users use this skill to simulate trips to real destinations, produce detailed day-by-day plans and first-person travel writing, and collect or generate supporting images for local trip files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live travel details, prices, opening hours, weather, and reviews may change after the itinerary is generated. <br>
Mitigation: Check current source pages before relying on the itinerary, especially for reservations, tickets, transit, and weather-sensitive plans. <br>
Risk: Trip files and images can contain sensitive future travel details or personal preferences. <br>
Mitigation: Avoid entering unnecessary sensitive travel details, review the generated trip folder, and delete it when the trip output is no longer needed. <br>
Risk: Real photos may carry reuse restrictions or attribution requirements. <br>
Mitigation: Verify image rights and attribution before sharing, publishing, or repackaging the generated travelogue. <br>
Risk: Immersive mode can preserve progress state and may be scheduled to continue work later. <br>
Mitigation: Review scheduled mode and checkpoint files before enabling or resuming an immersive trip. <br>


## Reference(s): <br>
- [Cyber Travel on ClawHub](https://clawhub.ai/axelhu/cyber-travel) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, images, configuration, guidance] <br>
**Output Format:** [Markdown trip files with optional HTML/PDF-ready content and local image references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plan.md, day{N}.md, optional state.md, summary.md, and image assets under a local trip folder when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
