## Description: <br>
Guides agents through requesting and configuring daily synchronization between ODPS/DataWorks warehouse tables and Feishu Bitable, including sync direction, form fields, field mapping, approvals, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, data engineers, and operations teams use this skill to prepare approved DataWorks-to-Bitable or Bitable-to-DataWorks synchronization requests, configure mappings and permissions, and troubleshoot failed sync tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Daily synchronization can clear or fully overwrite destination data. <br>
Mitigation: Confirm the sync direction, destination table or Bitable, capacity limits, and approvals before enabling or changing a scheduled job. <br>
Risk: Incorrect Feishu app or collaborator permissions could expose or alter sensitive business data. <br>
Mitigation: Verify the named sync app or collaborator group is the legitimate internal service and grant only the documented manage permission needed for the workflow. <br>
Risk: Sensitive warehouse data may require additional review before synchronization. <br>
Mitigation: Follow the documented approval flow, including sensitivity checks and extra business-owner approval where required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/dw-bitable-sync) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with tables, examples, and checklist-style instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution; outputs are configuration and review guidance for DataWorks and Feishu Bitable synchronization workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
