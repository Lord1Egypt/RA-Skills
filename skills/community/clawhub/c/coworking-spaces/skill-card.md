## Description: <br>
Find nearby coworking spaces. Invoke when user asks for shared offices near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask an agent to find nearby coworking or shared office options from a provided or authorized location, with optional radius, result-limit, and amenity filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a user's current or intended location, which may expose sensitive location data. <br>
Mitigation: Ask for location consent, prefer approximate locations where possible, and avoid retaining precise coordinates. <br>
Risk: The referenced STANDARD_RESPONSE.md response-schema file is not included in the package, so downstream output shape may be ambiguous. <br>
Mitigation: Confirm the expected point-of-interest fields before integrating results into frontends, APIs, or other downstream systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/coworking-spaces) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Markdown or structured point-of-interest list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses location, radius, result limit, and optional filters; category is fixed to coworking-spaces.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
