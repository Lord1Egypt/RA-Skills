## Description: <br>
Find nearby bars when the user asks for drinks or nightlife near them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to handle requests for nearby bars, drinks, or nightlife by collecting location and filter inputs and returning nearby bar or POI results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location-based searches can expose precise user coordinates if location is requested, logged, or retained unnecessarily. <br>
Mitigation: Request explicit location permission, avoid storing exact coordinates, and use coarse location handling or short-term caching only when needed. <br>
Risk: The skill may trigger on broad nightlife planning when the user did not ask for nearby bars. <br>
Mitigation: Invoke it only when the user asks for nearby bars, drinks, nightlife near them, or provides a location for bar recommendations. <br>


## Reference(s): <br>
- [Nearby Bars on ClawHub](https://clawhub.ai/CodeKungfu/bars) <br>
- [CodeKungfu publisher profile](https://clawhub.ai/user/CodeKungfu) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or structured text describing nearby bar or POI results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses location, radius, result limit, and optional filters such as open_now, minimum rating, price level, and keywords.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
