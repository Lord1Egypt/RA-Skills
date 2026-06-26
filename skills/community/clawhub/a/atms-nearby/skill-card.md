## Description: <br>
Find nearby ATMs when the user asks for cash withdrawal options near their current location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and location-aware app integrators use this skill to request nearby ATM points of interest from an authorized location, with radius, result limit, and optional ATM filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires user location data to find nearby ATMs. <br>
Mitigation: Request location only when needed, obtain user authorization, and avoid retaining precise coordinates except where necessary for the query. <br>
Risk: The referenced standard response schema is not included in the artifact. <br>
Mitigation: Verify the expected response fields before integrating the skill into a frontend, API, or downstream workflow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Structured point-of-interest response guidance with location, radius, limit, filters, category, and error code conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authorized latitude and longitude input; default radius is 3000 meters, default limit is 20, and maximum limit is 50.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
