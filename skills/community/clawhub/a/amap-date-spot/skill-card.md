## Description: <br>
Amap Date Spot helps an agent recommend conversation-friendly date, meetup, and casual business venues by using Amap location, POI, route, and weather data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongdongyue](https://clawhub.ai/user/dongdongyue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to choose date, friend meetup, matchmaking, anniversary, birthday, confession, or informal business meeting spots. It produces venue recommendations with rationale, route planning, parking notes, alternatives, and optional shareable planning outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports under-disclosed automatic file creation and extra map API credentials that may be embedded in generated HTML. <br>
Mitigation: Review generated files before sharing, generate HTML only when Amap JS credentials are approved for client-side use, and avoid exposing private API credentials in shareable pages. <br>
Risk: Meeting plans, exact routes, and CSV exports can contain sensitive personal location and relationship context. <br>
Mitigation: Use coarse locations unless exact routing is necessary, keep exported CSV and HTML files private, and remove sensitive details before sending plans to others. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/dongdongyue/amap-date-spot) <br>
- [ClawHub skill page](https://clawhub.ai/dongdongyue/skills/amap-date-spot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown recommendations, with optional CSV and HTML planning artifacts when requested by the user.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations may include venue rankings, route timing, weather-aware notes, parking guidance, backup options, itinerary steps, and shareable invitation text.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
