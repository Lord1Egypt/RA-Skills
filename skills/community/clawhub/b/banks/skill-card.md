## Description: <br>
Finds nearby bank branches when a user asks for banks near their current location. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to find nearby bank branches from an authorized location, with optional radius, result limit, and service filters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Precise location data can reveal sensitive user context if requested, retained, or reused unnecessarily. <br>
Mitigation: Request explicit location permission, use coordinates only for the nearby-bank query, and avoid retaining precise coordinates; apply grid-level fuzzing when retention is necessary. <br>
Risk: Integrations may rely on exact response fields that are not fully documented in the packaged skill because the linked standard response file is not included. <br>
Mitigation: Confirm the expected response schema before integration and handle the documented invalid-location, radius, provider, and rate-limit errors. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [Structured nearby-bank result list or documented error code.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-authorized location; category is fixed to banks.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
