## Description: <br>
Manage AWS EC2, S3, Lambda, and CloudWatch resources with deployment, operations, and monitoring guidance across AWS regions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to work with AWS infrastructure tasks such as EC2 instance lifecycle management, S3 object and bucket operations, Lambda function management, and CloudWatch monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad AWS capabilities and includes create, update, delete, terminate, upload, download, and invoke operations. <br>
Mitigation: Use a dedicated least-privilege IAM role or short-lived credentials, restrict accounts, regions, and resources, and require explicit confirmation before resource-changing operations. <br>
Risk: The package source is not backed by server-resolved GitHub provenance for this version. <br>
Mitigation: Verify the real package source before installation or use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaiyuelv/aws-cloud-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/kaiyuelv) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON schemas, Python examples, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AWS operations may require credentials, IAM permissions, target regions, and explicit confirmation for resource-changing actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
