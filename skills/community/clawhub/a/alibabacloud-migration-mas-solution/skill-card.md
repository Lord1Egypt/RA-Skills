## Description: <br>
Generates Alibaba Cloud migration plans from AWS, Azure, Huawei Cloud, or Tencent Cloud product inventories, including product mapping, migration steps, risk notes, and deliverable documents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, migration engineers, and cloud architects use this skill to turn source-cloud product lists or resource inventories into Alibaba Cloud migration-plan drafts. It is intended for cross-cloud migrations from AWS, Azure, Huawei Cloud, or Tencent Cloud to Alibaba Cloud, including product mapping, official-documentation-backed steps, risk assessment, reverse sync planning, and optional Word conversion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated migration guidance may be incomplete for production workloads if it is used directly from product mappings without a reviewed runbook. <br>
Mitigation: Require a reviewed migration runbook with backup and rollback plans, maintenance-window planning, and post-migration validation before real migrations. <br>
Risk: Cloud migration work can expose credentials, data in transit, or transferred data if operational controls are weak. <br>
Mitigation: Use least-privilege temporary credentials, encrypted transfer and storage, integrity checks, and environment-specific security review. <br>


## Reference(s): <br>
- [AWS Product to Alibaba Cloud Product Mapping and Migration Methods](references/aws-product-mapping.md) <br>
- [Azure Product to Alibaba Cloud Product Mapping and Migration Methods](references/azure-product-mapping.md) <br>
- [Huawei Cloud Product to Alibaba Cloud Product Mapping and Migration Methods](references/huawei-product-mapping.md) <br>
- [Tencent Cloud Product to Alibaba Cloud Product Mapping and Migration Methods](references/tencent-product-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Files, Shell commands] <br>
**Output Format:** [Markdown migration plan with an optional DOCX file generated from the Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plans should include official Alibaba Cloud documentation links, migration risks, mitigation measures, reverse synchronization guidance, and the generated DOCX path when conversion is run.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
