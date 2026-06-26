## Description: <br>
Find nearby camping sites. Invoke when user asks for camping near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to find nearby camping, campsite, and RV-site points of interest from an authorized location, radius, limit, and optional filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Campsite search requests can expose sensitive location data. <br>
Mitigation: Use only user-authorized location data, prefer a city or approximate coordinates when exact location is unnecessary, and keep any cache short-lived and coarse. <br>
Risk: External place data may be unavailable, rate limited, or stale. <br>
Mitigation: Surface provider-unavailable and rate-limited errors clearly and ask users to verify campsite details before travel. <br>


## Reference(s): <br>
- [ClawHub listing for Nearby Camping Sites](https://clawhub.ai/CodeKungfu/camping-sites) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured POI response guidance with standardized fields and error codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Category is fixed to camping-sites; location, radius, limit, and optional filters shape the response.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
