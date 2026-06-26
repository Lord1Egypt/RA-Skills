## Description: <br>
Enforce cloud resource tagging policies for cost allocation, compliance, and governance across AWS/GCP/Azure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud administrators, platform engineers, and FinOps or compliance teams use this skill to audit AWS, GCP, and Azure resource tags, define tagging policies, generate compliance reports, and prepare remediation scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated remediation scripts can change cloud resource tags in production environments if run without review. <br>
Mitigation: Confirm the active account, project, or subscription, replace placeholder values, narrow the resource scope, and route changes through normal owner review and approval before applying tags. <br>
Risk: Discovery commands may expose cloud inventory details while auditing tag compliance. <br>
Mitigation: Prefer read-only credentials for discovery and handle generated reports according to the organization's cloud governance and data handling policies. <br>


## Reference(s): <br>
- [Cloud Tag Enforcer on ClawHub](https://clawhub.ai/charlie-morrison/cloud-tagging-enforcer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell and code blocks, report templates, and remediation script examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cloud-provider-specific audit, policy, and remediation guidance; generated commands require user review before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
