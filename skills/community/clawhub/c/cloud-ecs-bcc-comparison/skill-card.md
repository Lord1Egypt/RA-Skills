## Description: <br>
云主机询价小能手对标阿里云 ECS 与百度智能云 BCC 规格，并查询预付费 1 个月的云主机、磁盘和公网带宽价格。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[963029755](https://clawhub.ai/user/963029755) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud cost analysts, and procurement teams use this skill to collect cloud VM requirements, run pricing commands, and compare equivalent one-month prepaid Alibaba Cloud ECS and Baidu BCC configurations. <br>

### Deployment Geography for Use: <br>
Global; the included region mapping focuses on mainland China and Hong Kong cloud regions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles Alibaba Cloud and Baidu Cloud access keys. <br>
Mitigation: Use least-privilege or temporary read-only pricing credentials, and avoid pasting administrator cloud keys into chat. <br>
Risk: Baidu-side credential transport and pricing responses are unsafe while TLS verification is disabled. <br>
Mitigation: Inspect or patch the referenced script to restore TLS certificate verification before relying on Baidu-side results. <br>
Risk: The skill references sibling setup scripts for credential configuration. <br>
Mitigation: Inspect the referenced setup scripts before running them and confirm where credentials are stored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/963029755/cloud-ecs-bcc-comparison) <br>
- [Alibaba Cloud ECS DescribePrice API](https://help.aliyun.com/zh/ecs/developer-reference/api-ecs-2014-05-26-describeprice) <br>
- [Baidu Intelligent Cloud BCC instance families](https://cloud.baidu.com/doc/BCC/s/wjwvynogv) <br>
- [Baidu Intelligent Cloud BCC price query API](https://cloud.baidu.com/doc/BCC/s/uk5dt23r8) <br>
- [Baidu Intelligent Cloud CDS price query API](https://cloud.baidu.com/doc/BCC/s/blu16n1zm) <br>
- [Baidu Intelligent Cloud EIP price query API](https://cloud.baidu.com/doc/EIP/s/Hk9gy7w7q) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and tabular price comparison text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are constrained to one-month prepaid pricing; traffic-based bandwidth is shown as a unit price and excluded from monthly totals.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
