## Description: <br>
Query AWS (Amazon Web Services) product information, documentation, parameters, features, and pricing from official sources without login. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangbingpeng](https://clawhub.ai/user/wangbingpeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud architects, and AWS users use this skill to identify AWS services, find official documentation, compare service capabilities, and gather pricing or quick-start guidance in English or Chinese. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated AWS CLI or SDK examples may create resources, change cloud configuration, or incur cost if run without review. <br>
Mitigation: Review IAM permissions, region, network exposure, and cost impact before running commands or code; only execute snippets when you explicitly intend to create or modify AWS resources. <br>
Risk: Prompts or generated snippets may encourage handling AWS credentials directly. <br>
Mitigation: Do not paste real AWS keys into prompts or hardcode them in generated code; prefer AWS profiles, SSO, IAM roles, or the default credential chain. <br>


## Reference(s): <br>
- [AWS product pages](https://aws.amazon.com/) <br>
- [AWS documentation](https://docs.aws.amazon.com/) <br>
- [AWS pricing](https://aws.amazon.com/pricing/) <br>
- [AWS CLI command reference](https://docs.aws.amazon.com/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with tables and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include AWS CLI or SDK examples that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
