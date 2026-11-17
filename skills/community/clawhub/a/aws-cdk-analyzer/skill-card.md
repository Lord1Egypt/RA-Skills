## Description:

Analyze AWS CDK applications for best practices, security, cost optimization, and deployment safety - covers construct patterns, IAM policies, and CloudFormation output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure engineers use this skill to review AWS CDK applications before deployment or during audits, focusing on security, cost, best practices, and deployment safety.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask an agent to run AWS CDK synth or diff commands, which can execute project code and use existing AWS access.

Mitigation: Use the skill only on trusted CDK projects or inside an isolated environment, prefer a lockfile-verified local CDK install with npx --no-install, remove unrelated secrets and AWS credentials, and use a narrowly scoped read-only AWS role only when live diff access is explicitly needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with severity-ranked findings, recommendations, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include security issues, cost estimates, best-practice findings, deployment safety notes, and remediation guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
