## Description:

Manages Tencent Cloud COS vector buckets, indexes, vector data, and bucket policies across their lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmyyan](https://clawhub.ai/user/jimmyyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to perform Tencent Cloud COS vector storage operations, including bucket, index, policy, and vector data management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Tencent Cloud credentials.

Mitigation: Use least-privilege credentials and secure environment or secret injection instead of passing secrets on the command line.

Risk: The skill can perform destructive bucket, index, vector, and bucket-policy operations.

Mitigation: Manually confirm delete and bucket-policy actions before allowing an agent to run them.

Risk: The shared connection option defaults to plain HTTP.

Mitigation: Force HTTPS for every Tencent Cloud COS vector call.

## Reference(s):

- [COS Vector Bucket API Reference](artifact/references/api_reference.md)
- [Tencent Cloud COS Vector Bucket Documentation](https://cloud.tencent.com/document/product/436/127755)
- [ClawHub Skill Page](https://clawhub.ai/jimmyyan/skills/cos-vectors-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud COS vector credentials plus region and bucket inputs; scripts return JSON success or error objects.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
