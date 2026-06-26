## Description: <br>
Analyze AWS CDK applications for best practices, security, cost optimization, and deployment safety - covers construct patterns, IAM policies, and CloudFormation output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure engineers use this skill to review AWS CDK applications, IAM policies, construct patterns, resource configuration, cost risks, and deployment safety before release or during infrastructure audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CDK and IAM review can expose sensitive infrastructure details while analyzing the target repository or stack. <br>
Mitigation: Use the skill only on repositories and stacks intended for review, and avoid sharing generated analysis outside the authorized project team. <br>
Risk: Suggested CDK, IAM, or deployment changes may affect security, cost, or data retention if applied without review. <br>
Mitigation: Have an infrastructure owner review recommendations and run normal CDK diff, change-set, and deployment approval checks before applying changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/aws-cdk-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with findings, recommendations, tables, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings may be grouped by severity, cost optimization, and good practices.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
