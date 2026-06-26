## Description: <br>
Find nearby cinemas. Invoke when user asks for movie theaters near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent builders use this skill to request nearby movie theaters from an authorized location, with configurable radius, result limits, and optional filters such as IMAX, rating, and open status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sharing precise location can expose sensitive location data. <br>
Mitigation: Request location only when the user wants nearby cinema results, prefer approximate location when sufficient, and avoid retaining exact coordinates. <br>
Risk: The skill references a local STANDARD_RESPONSE.md path that is not packaged with this release. <br>
Mitigation: Publisher should inline or package response-format details so downstream agents can apply the intended standardized fields. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mikeclaw007/cinemas) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, JSON] <br>
**Output Format:** [Structured text or JSON-like point-of-interest results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-authorized location input; default radius is 3000 meters, default result limit is 20, and maximum result limit is 50.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
