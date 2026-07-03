## Description: <br>
Maps AWS, Tencent Cloud, Huawei Cloud, and Azure resources to Alibaba Cloud products and instance specifications, including usage conversion and Alibaba Cloud price estimates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud migration engineers, and cost analysts use this skill to map resource inventories or bills from AWS, Tencent Cloud, Huawei Cloud, and Azure to Alibaba Cloud equivalents. It produces product mappings, instance-spec comparisons, migration priority guidance, and reference cost estimates after confirming the source vendor and Alibaba Cloud target region. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The pricing helper uses Alibaba Cloud credentials through an unauthenticated network service. <br>
Mitigation: Run it only in a trusted local environment, bind it to localhost when possible, stop it after use, and avoid untrusted or non-HTTPS remote pricing URLs. <br>
Risk: Credential exposure or over-permissioning could affect Alibaba Cloud resources or billing data. <br>
Mitigation: Use a dedicated least-privilege RAM account with only the pricing and describe permissions needed for the migration estimate workflow. <br>
Risk: Pricing or mapping output may include unavailable specs, failed quote lookups, or reference prices rather than contract prices. <br>
Mitigation: Review fallback annotations, confirm the target region, and verify final pricing with Alibaba Cloud sales or the official console before making migration decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-migration-mas-product-mapping) <br>
- [Alibaba Cloud default credential provider chain](https://help.aliyun.com/document_detail/378659.html) <br>
- [Required RAM permissions](references/ram-policies.md) <br>
- [Alibaba Cloud pricing API index](references/pricing-api.md) <br>
- [AWS product and spec mappings](references/mappings/aws.md) <br>
- [Azure product and spec mappings](references/mappings/azure.md) <br>
- [Huawei Cloud product and spec mappings](references/mappings/huawei.md) <br>
- [Tencent Cloud product and spec mappings](references/mappings/tencent.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and summaries, with optional Excel output files and shell commands for the pricing helper] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include real-time Alibaba Cloud pricing, fallback annotations, region-specific estimates, and manual verification notes for unavailable specs or prices.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
