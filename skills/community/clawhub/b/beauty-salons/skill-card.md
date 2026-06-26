## Description: <br>
Find nearby beauty salons. Invoke when user asks for beauty services near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find nearby beauty salons from a provided location or city and narrow results by rating, price level, open status, or keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses user location data to search for nearby salons. <br>
Mitigation: Ask for location permission, prefer approximate location when exact coordinates are unnecessary, and avoid retaining precise coordinates. <br>
Risk: Repeated location-based searches could expose precise movement patterns or increase provider request volume. <br>
Mitigation: Use short-term caching for location, category, and radius combinations, and apply coordinate anonymization where appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/beauty-salons) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, JSON] <br>
**Output Format:** [Text or structured JSON describing nearby beauty salon points of interest] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns standardized POI fields for the beauty-salons category and may include error codes for invalid location, excessive radius, provider unavailability, or rate limiting.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
