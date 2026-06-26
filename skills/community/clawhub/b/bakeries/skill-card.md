## Description: <br>
Find nearby bakeries. Invoke when user asks for bakeries near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to find nearby bakeries from a user-approved location, with optional filters such as distance, open-now status, rating, price level, and keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill may require sharing precise or approximate user location to find nearby bakeries. <br>
Mitigation: Request location permission before lookup, prefer approximate location when exact coordinates are not necessary, and avoid retaining precise coordinates beyond the immediate search. <br>
Risk: Repeated nearby searches can expose sensitive movement patterns if precise coordinates are stored or reused broadly. <br>
Mitigation: Use coordinate fuzzing or grid-based approximation when appropriate, and limit any location-based caching to short-lived entries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawkk/bakeries) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/clawkk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, JSON] <br>
**Output Format:** [Text or structured JSON-style point-of-interest results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns bakery-category results with location, radius, limit, and optional filter handling.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
