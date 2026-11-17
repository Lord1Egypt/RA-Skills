## Description: <br>
Aws Cloud Inspector Free is an AWS CLI-based cloud infrastructure inspection assistant for resource inventory, health checks, and basic security checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to inspect AWS accounts through AWS CLI commands for resource inventory, health checks, basic security checks, region/profile troubleshooting, and dry-run previews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is labeled read-only but also permits user-confirmed write or destructive AWS operations. <br>
Mitigation: Review every AWS CLI command before execution, prefer dry-run previews, and use a dedicated read-only IAM role or profile. <br>
Risk: AWS CLI commands may affect the wrong account, profile, or region if context is unclear. <br>
Mitigation: Confirm identity with aws sts get-caller-identity and explicitly set the intended AWS profile and region before running inspection commands. <br>
Risk: AWS credential exposure could occur if local credential files or secret environment variables are printed. <br>
Mitigation: Do not display credential files, access keys, or session tokens; rely on AWS CLI's credential handling. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/aws-cloud-inspector-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [AWS CLI commands should be reviewed before execution; AWS credentials are handled by AWS CLI profiles and should not be printed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
