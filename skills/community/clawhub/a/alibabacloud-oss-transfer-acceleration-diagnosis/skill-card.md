## Description:

Read-only OSS transfer acceleration diagnosis that detects when acceleration is not taking effect, separates OSS Data Accelerator from Transfer Acceleration, and explains cross-border slowness and fee semantics without changing cloud resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to diagnose Alibaba Cloud OSS transfer acceleration adoption, endpoint misuse, cross-border or cross-region access slowness, product-selection confusion, and transfer acceleration fee semantics. The skill produces evidence-based findings from read-only OSS metadata queries and packaged reference guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use configured Alibaba Cloud credentials to list account bucket names during fallback lookup.

Mitigation: Run it with a narrowly scoped read-only RAM role and provide the exact bucket name so bucket enumeration is avoided unless fallback lookup is needed.

Risk: The skill asks operators to upgrade the local Alibaba Cloud CLI before use.

Mitigation: Verify the active Alibaba Cloud profile first and approve any `aliyun` CLI upgrade as a separate local change before running diagnostics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-oss-transfer-acceleration-diagnosis)
- [M1: Adoption Decision Tree](references/adoption-decision-tree.md)
- [M2: OSS Data Accelerator vs Transfer Acceleration](references/accelerator-vs-transfer-acceleration.md)
- [M3: Transfer Acceleration Fee Fact Sheet](references/fee-facts.md)
- [Minimal Read-Only RAM Policy](references/ram-policies.md)
- [Alibaba Cloud OSS transfer acceleration documentation](https://help.aliyun.com/zh/oss/user-guide/transfer-acceleration)
- [Alibaba Cloud OSS value-added billing items](https://help.aliyun.com/zh/oss/value-added-billing-item/)
- [GetBucketTransferAcceleration API reference](https://help.aliyun.com/zh/oss/developer-reference/getbuckettransferacceleration)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with structured status, findings, next action, and cited documentation links when verification is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic output based on included scripts, OSS metadata responses, and bundled product-reference material.]

## Skill Version(s):

0.0.1 (source: references/manifest.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
