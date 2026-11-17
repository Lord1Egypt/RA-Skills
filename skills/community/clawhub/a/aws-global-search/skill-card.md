## Description:

Query AWS (Amazon Web Services) product information, documentation, parameters, features, and pricing from official sources without login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangbingpeng](https://clawhub.ai/user/wangbingpeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and cloud practitioners use this skill to identify AWS services, retrieve official documentation and pricing, compare services, and prepare bilingual AWS product summaries or implementation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Copyable AWS examples can create billable resources when run against a real AWS account.

Mitigation: Review commands before execution, use least-privilege credentials in a non-production account when possible, understand expected costs, and plan cleanup first.

Risk: AWS credential examples could lead users to paste real access keys into prompts or shared snippets.

Mitigation: Keep credentials as placeholders, do not paste real AWS access keys into examples, and prefer IAM roles or local credential configuration.

Risk: Pricing and service details can become stale or vary by region.

Mitigation: Verify pricing and service limits against official AWS pricing pages or documentation before making purchasing or deployment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangbingpeng/skills/aws-global-search)
- [AWS homepage](https://aws.amazon.com/)
- [AWS China](https://www.amazonaws.cn/)
- [AWS documentation](https://docs.aws.amazon.com/)
- [AWS pricing](https://aws.amazon.com/pricing/)
- [AWS CLI command reference](https://docs.aws.amazon.com/cli/)
- [AWS Pricing Calculator](https://calculator.aws/)
- [Examples](artifact/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown with bilingual product summaries, tables, links, and optional code or shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pricing estimates, API references, AWS CLI or SDK examples, and credential placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
