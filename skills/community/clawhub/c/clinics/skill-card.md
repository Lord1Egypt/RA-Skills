## Description: <br>
Finds nearby clinics when a user asks for a clinic near them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to request nearby clinic options for a provided location, radius, result limit, and optional filters such as open_now or min_rating. Integrators can use its standardized point-of-interest response shape for frontend or API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Server security evidence marks the release suspicious and calls for review before installation. <br>
Mitigation: Review the skill and its artifact before deployment; install it only when its documented nearby-clinic workflow matches the intended use. <br>
Risk: The artifact handles precise user location values for clinic search. <br>
Mitigation: Query only after user authorization, avoid retaining precise coordinates, and use coarse or grid-based location handling where feasible. <br>
Risk: The artifact describes provider unavailability and rate-limit errors. <br>
Mitigation: Handle PROVIDER_UNAVAILABLE and RATE_LIMITED responses explicitly, and use short-term caching for repeated location/category/radius requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/clinics) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/CodeKungfu) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured point-of-interest response guidance with JSON-like inputs and outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns clinic search results using a fixed clinics category and documented error codes.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
