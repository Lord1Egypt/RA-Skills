## Description: <br>
BigFish is an AI fishing assistant that analyzes fishing spot images, combines weather and location context, recommends target fish, techniques, bait, and trip timing, and helps record fishing reports and catch data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobenfang](https://clawhub.ai/user/kobenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Fishing hobbyists and outdoor anglers use this skill to evaluate fishing spots, decide when and how to fish, and keep structured records of trips and catches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate during casual fishing questions when the user did not intend to invoke fishing-analysis behavior. <br>
Mitigation: Use explicit phrasing when asking casual fishing questions, and invoke the skill only when fishing analysis or catch-record support is desired. <br>
Risk: Fishing spot analysis can involve location or weather context that may require user permission or disclose sensitive trip details. <br>
Mitigation: Review permission prompts before allowing location or weather access, and share only the location detail needed for the fishing recommendation. <br>


## Reference(s): <br>
- [BigFish on ClawHub](https://clawhub.ai/kobenfang/bigfish) <br>
- [Weather skill](https://clawhub.ai/skills/weather) <br>
- [Bigseed skill](https://clawhub.ai/skills/bigseed) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured recommendations, ratings, and fishing-report entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for user-provided images, city or location, weather context, and catch details; no environment variables are required.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
