## Description: <br>
Plan and optimize domestic China trips using flyai/Fliggy search, public metro-network data, and optional itinerary page generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gushuaialan1](https://clawhub.ai/user/gushuaialan1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to turn domestic China trip requests into practical itineraries with transport options, hotel-area guidance, attraction picks, budget considerations, crowd-avoidance notes, and day-by-day scheduling. Developers can also use it to produce structured trip data and standalone HTML itinerary pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional page-publishing flow can change files and push a GitHub Pages branch. <br>
Mitigation: Run build, init, and deploy commands only in a dedicated workspace; before deployment, verify the repository is clean and confirm the target remote and staged files. <br>
Risk: Generated travel plans may contain inaccurate or stale booking, route, pricing, or availability details from external travel search sources. <br>
Mitigation: Review itinerary details, booking links, dates, prices, transit routes, and hotel recommendations before relying on or sharing the plan. <br>


## Reference(s): <br>
- [Skill README](artifact/README.md) <br>
- [Domestic planning prompt patterns](artifact/references/domestic-planning-prompts.md) <br>
- [Subway-aware planning](artifact/references/subway-aware-planning.md) <br>
- [Structured Output Mode](artifact/references/structured-output-mode.md) <br>
- [Travel Page Framework README](artifact/page-generator/README.md) <br>
- [Trip content guidelines](artifact/page-generator/schema/trip-content-guidelines.md) <br>
- [Trip data JSON schema](artifact/page-generator/schema/trip-schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance] <br>
**Output Format:** [Markdown travel plans with optional structured JSON trip data, shell commands, and generated static HTML itinerary files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include booking or detail links from flyai/Fliggy results and free-license image metadata from Wikimedia Commons when those tools are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
