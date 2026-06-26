## Description: <br>
Find nearby car parks when a user asks for parking near their current location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request nearby car parks from a current location, with optional radius, limit, and parking filters. It is intended to return a standardized point-of-interest list for interface or API integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs location data to find nearby parking. <br>
Mitigation: Only grant location access while actively searching for parking, and avoid retaining precise coordinates; use obfuscation when precision is not required. <br>
Risk: The referenced standard response schema is not included in the release artifact. <br>
Mitigation: Review the expected response contract before integration so downstream interfaces handle fields and errors consistently. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikeclaw007/car-parks) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance describing JSON-like request and response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-authorized location input; recommends avoiding retention of precise coordinates and using coordinate obfuscation when needed.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
