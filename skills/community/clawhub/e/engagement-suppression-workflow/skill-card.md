## Description: <br>
Builds a two-tier HubSpot sunset workflow that re-engages dormant contacts before suppressing contacts who remain inactive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operations and revenue operations teams use this skill to design and verify a HubSpot re-engagement workflow that protects deliverability while giving inactive contacts a chance to re-engage before suppression. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect HubSpot enrollment filters or AND/OR trigger logic could suppress the wrong contacts. <br>
Mitigation: Review the HubSpot filters, preview affected contacts, test on a small segment, and manually verify trigger logic before turning on the workflow. <br>
Risk: Browser-extension or AI-assisted workflow setup could make business-impacting changes before the workflow is reviewed. <br>
Mitigation: Supervise automation, keep the workflow disabled until review is complete, and confirm rollback steps before activation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomgranot/engagement-suppression-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, Text] <br>
**Output Format:** [Markdown guidance with workflow steps and prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes configurable inactivity and re-engagement windows; no files or API calls are generated.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
