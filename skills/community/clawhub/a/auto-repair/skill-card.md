## Description: <br>
Find nearby auto repair. Invoke when user asks for car repair near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mikeclaw007](https://clawhub.ai/user/mikeclaw007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and assistant agents use this skill to structure nearby auto repair lookup from an authorized user location, including radius, limit, filter inputs, and consistent POI-style results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on precise user location to find nearby services. <br>
Mitigation: Query only after user location authorization and avoid retaining exact coordinates; use coarse or grid-blurred coordinates when persistence is needed. <br>
Risk: The referenced STANDARD_RESPONSE.md is not included, so the full response contract is not inspectable from this artifact. <br>
Mitigation: Confirm the expected response schema before integrating the skill into an interface or downstream workflow. <br>
Risk: Provider availability, invalid coordinates, large radii, or rate limits may prevent useful results. <br>
Mitigation: Handle the declared error codes and keep radius and result limits within the documented defaults and maximums. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mikeclaw007/auto-repair) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Markdown instructions with structured input and response field guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defines location, radius, limit, filters, category, and expected error codes for nearby auto repair lookup.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
