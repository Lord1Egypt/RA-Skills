## Description:

Manage AWS EC2, S3, Lambda, and CloudWatch resources with automated deployment, operations, and monitoring across multiple regions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaiyuelv](https://clawhub.ai/user/kaiyuelv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to manage AWS compute, storage, serverless, and monitoring resources through agent-assisted commands, code examples, and configuration guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes broad AWS permissions and destructive operations such as terminate, delete, update, upload, and invoke.

Mitigation: Use least-privilege and preferably short-lived AWS credentials, scope IAM permissions to required resources, and require explicit confirmation before running destructive operations against real AWS resources.

Risk: Server security evidence reports limited provenance and warns against the placeholder repository or unverified package name.

Mitigation: Install only from a verified source and avoid relying on the placeholder repository or unverified package name.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaiyuelv/skills/aws-cloud-toolkit)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact requirements](artifact/requirements.txt)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, Python, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes AWS operation examples, environment variable guidance, dependency requirements, and IAM permission notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
