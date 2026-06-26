## Description: <br>
Find nearby cafes when the user asks for coffee nearby. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request nearby cafe or coffee-place results from an authorized location, with optional radius, limit, and cafe filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use location data to find nearby cafes. <br>
Mitigation: Share only a one-time or coarse location, and avoid retaining precise coordinates beyond the request. <br>
Risk: The referenced STANDARD_RESPONSE.md file is not included in the artifact, so exact response formatting may be unclear. <br>
Mitigation: Publisher should bundle the missing response-format reference or define the expected output fields directly in the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikeclaw007/cafes) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Structured place-result guidance with standardized cafe category, fields, and error codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-authorized location; supports radius, result limit, and optional cafe filters.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
