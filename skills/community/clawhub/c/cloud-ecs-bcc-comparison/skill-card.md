## Description:

Compares Alibaba Cloud ECS and Baidu Intelligent Cloud BCC cloud host pricing for matched CPU, memory, disk, bandwidth, and region inputs, limited to one-month prepaid quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[963029755](https://clawhub.ai/user/963029755)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud engineers, and infrastructure buyers use this skill to collect cloud host requirements, map comparable Alibaba Cloud ECS and Baidu Intelligent Cloud BCC specifications, run pricing commands, and review one-month prepaid price comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles cloud access credentials and may prompt users to provide long-lived access keys.

Mitigation: Use least-privilege, read-only pricing credentials, avoid pasting long-lived secrets into chat or command lines, and rotate any keys already shared that way.

Risk: Authenticated Baidu Cloud API calls are made without TLS certificate verification.

Mitigation: Do not rely on Baidu Cloud results until TLS verification is fixed; validate prices through trusted provider channels before making purchase decisions.

Risk: Traffic-based bandwidth output and sold-out fallback behavior may be inconsistent with the documented prepaid-only promise.

Mitigation: Confirm billing mode, bandwidth treatment, and any fallback instance generation directly with the cloud provider before using the comparison commercially.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/963029755/skills/cloud-ecs-bcc-comparison)
- [Alibaba Cloud ECS DescribePrice API](https://help.aliyun.com/zh/ecs/developer-reference/api-ecs-2014-05-26-describeprice)
- [Baidu Intelligent Cloud BCC instance families](https://cloud.baidu.com/doc/BCC/s/wjwvynogv)
- [Baidu Intelligent Cloud BCC price query API](https://cloud.baidu.com/doc/BCC/s/uk5dt23r8)
- [Baidu Intelligent Cloud CDS price query API](https://cloud.baidu.com/doc/BCC/s/blu16n1zm)
- [Baidu Intelligent Cloud EIP price query API](https://cloud.baidu.com/doc/EIP/s/Hk9gy7w7q)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and command-line text tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs one-month prepaid price comparisons; traffic-based bandwidth is described separately and is not included in monthly totals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
