## Description: <br>
Audit and remove unused, test, or deprecated forms from HubSpot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HubSpot administrators and marketing operations teams use this skill to inventory forms, identify unused or test assets, and document cleanup decisions before deletion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HubSpot form deletion removes the form definition and deleted forms cannot be restored. <br>
Mitigation: Generate an inventory, export form definitions before deletion, and manually approve every deletion. <br>
Risk: A broadly scoped HubSpot token could allow unintended form administration. <br>
Mitigation: Use a scoped HubSpot token only for the intended cleanup work. <br>


## Reference(s): <br>
- [Cleanup Forms on ClawHub](https://clawhub.ai/tomgranot/cleanup-forms) <br>
- [Publisher profile: tomgranot](https://clawhub.ai/user/tomgranot) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown guidance with a Python code example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a scoped HubSpot API token, inventory review, manual deletion approval, and cleanup logging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
