## Description: <br>
Find nearby conference centers. Invoke when user asks for conference venues near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to find nearby conference centers, event venues, and activity spaces from an authorized location or city-level query. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Venue searches can expose precise location data. <br>
Mitigation: Use approximate coordinates or a city-level location when exact proximity is not required, and query only after user location authorization. <br>
Risk: Provider errors, rate limits, or unavailable data sources can prevent complete venue results. <br>
Mitigation: Handle INVALID_LOCATION, RADIUS_TOO_LARGE, PROVIDER_UNAVAILABLE, and RATE_LIMITED responses, and apply short-term caching for repeated location, category, and radius queries. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/CodeKungfu/conference-centers) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or structured text describing nearby conference-center results and query constraints] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses location, radius, limit, and optional rating, price, or keyword filters; category is fixed to conference-centers.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
