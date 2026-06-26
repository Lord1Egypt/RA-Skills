## Description: <br>
Find nearby ATMs. Invoke when user asks for cash withdrawal near me. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask an agent to find nearby cash-withdrawal ATMs from their current location, with optional filters such as deposit support, fee-free access, radius, and result limit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs user location to find nearby ATMs. <br>
Mitigation: Request location only with user consent and avoid retaining precise coordinates; use grid-based anonymization when needed. <br>
Risk: The referenced STANDARD_RESPONSE.md file is not bundled, so exact response formatting may be unclear. <br>
Mitigation: Confirm the expected response fields before depending on integrations, or document a local fallback schema for POI results and errors. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/atms) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured POI results or error codes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-authorized location input; radius defaults to 3000 meters; result limit defaults to 20 and maxes at 50.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
