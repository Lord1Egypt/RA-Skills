## Description: <br>
Audit and remove inactive, test, or deprecated HubSpot workflows, including workflows with no enrollments, workflows turned off for 90+ days, and test workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HubSpot administrators and operations teams use this skill to inventory workflows, flag inactive or test automations, and plan cleanup with owner notification and deletion safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HubSpot API tokens may be exposed or over-scoped when inventorying workflows through the API. <br>
Mitigation: Use a HubSpot token limited to the minimum workflow permissions and keep it out of chat, logs, and generated documentation. <br>
Risk: Deleted HubSpot workflows cannot be restored, and removing the wrong workflow can disrupt business automation. <br>
Mitigation: Manually review every deletion candidate, document or screenshot workflow logic, notify owners, turn workflows off before deletion, and approve each deletion explicitly. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with a Python API example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human review before disabling or deleting workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
