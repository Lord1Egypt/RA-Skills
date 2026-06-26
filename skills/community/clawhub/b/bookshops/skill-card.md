## Description: <br>
Find nearby bookshops. Invoke when user asks for bookstores near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to find nearby bookshops, secondhand bookstores, and reading spaces from an authorized location or city query with consistent filters and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise user location could be over-collected or retained longer than needed. <br>
Mitigation: Use the least precise location that satisfies the request, prefer approximate location when possible, and keep any location-based cache short-lived. <br>
Risk: Provider outages or rate limits can prevent reliable nearby-bookshop results. <br>
Mitigation: Return the documented PROVIDER_UNAVAILABLE or RATE_LIMITED error instead of inventing results, and retry only within the provider's limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/clawkk/bookshops) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Markdown or JSON-style standardized POI list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes location, radius, limit, and optional filters such as open_now, min_rating, and keywords.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
