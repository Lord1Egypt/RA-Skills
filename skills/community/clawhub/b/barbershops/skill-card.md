## Description: <br>
Find nearby barbershops. Invoke when user asks for a haircut near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find nearby barbershops from an authorized location, optionally filtered by rating, price level, open status, or keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs user location data to find nearby barbershops. <br>
Mitigation: Request location authorization before use, prefer approximate or fuzzed coordinates when exact location is unnecessary, and avoid retaining precise coordinates beyond short-term caching. <br>
Risk: Nearby search results can be unavailable, rate limited, or constrained by invalid location input. <br>
Mitigation: Use the documented error codes for invalid location, excessive radius, provider unavailability, and rate limiting so callers can handle failures clearly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawkk/barbershops) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text] <br>
**Output Format:** [Structured text describing standardized place results, filters, and error codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-approved location data and returns the barbershops category.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
