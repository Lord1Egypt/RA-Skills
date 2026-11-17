## Description: <br>
aws-infra-free helps agents run read-only AWS CLI inventory and health-check queries for EC2, S3, RDS, and CloudWatch. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect AWS resource inventory and basic health status without creating, modifying, or deleting cloud resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes AWS CLI execution for cloud inventory commands. <br>
Mitigation: Use least-privilege AWS read-only credentials and keep agent execution within the documented inventory and health-check queries. <br>
Risk: Optional callback URLs may send completion data outside the local environment. <br>
Mitigation: Omit callback_url unless it points to a trusted HTTPS endpoint approved for the data being handled. <br>
Risk: Changing the global AWS CLI region can affect later AWS commands in the same environment. <br>
Mitigation: Prefer per-command --region flags instead of changing global AWS CLI configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/aws-infra-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with AWS CLI command snippets and table or JSON result expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for read-only AWS inventory and health-check workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
