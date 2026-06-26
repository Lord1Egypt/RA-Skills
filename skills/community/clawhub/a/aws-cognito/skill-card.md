## Description: <br>
Helps agents build, configure, debug, and secure AWS Cognito user pools, identity pools, authentication flows, federation, Lambda triggers, and integrations with AWS services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[encryptshawn](https://clawhub.ai/user/encryptshawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design AWS Cognito architectures, generate IaC and SDK implementation patterns, configure authentication flows, troubleshoot deployments, and review security settings before production use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Cognito or IAM examples can create overly broad permissions, unsafe callback URLs, or incorrect token handling if deployed without review. <br>
Mitigation: Review IAM permissions, callback and logout URLs, token storage and validation, and Lambda trigger behavior before deployment. <br>
Risk: Long-lived AWS credentials or live user passwords could be exposed if pasted into prompts, code, logs, or commits. <br>
Mitigation: Prefer AWS SSO, IAM roles, or short-lived credentials, and do not paste or commit long-lived AWS keys or live user passwords. <br>


## Reference(s): <br>
- [AWS Cognito Skill](SKILL.md) <br>
- [Cognito Authentication Flows](references/auth-flows.md) <br>
- [Cognito Infrastructure as Code Patterns](references/iac-patterns.md) <br>
- [Cognito Lambda Triggers](references/lambda-triggers.md) <br>
- [Cognito Security Best Practices](references/security.md) <br>
- [Cognito Setup Guide](references/setup-guide.md) <br>
- [Cognito Troubleshooting Guide](references/troubleshooting.md) <br>
- [ClawHub skill page](https://clawhub.ai/encryptshawn/aws-cognito) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AWS CDK, CloudFormation, Terraform, AWS SDK, Amplify, Lambda trigger, and IAM examples that require review before deployment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
