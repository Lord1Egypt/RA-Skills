## Description: <br>
Use the main local camofox-browser service for standard browser automation in this workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lotfinity](https://clawhub.ai/user/lotfinity) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to route standard browser automation work to the main local Camofox browser service and follow its snapshot-after-action workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs browser automation through a local service that may receive userId and sessionKey values. <br>
Mitigation: Confirm that 127.0.0.1:9377 is the intended local Camofox browser service before use and only share session values with trusted local services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lotfinity/camofox-browser-main) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration] <br>
**Output Format:** [Markdown instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Targets a local Camofox service at http://127.0.0.1:9377; userId is required and sessionKey is preferred.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
