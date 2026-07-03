## Description: <br>
Provides expert assistance for Alibaba Cloud Realtime Compute for Flink, including product parameters, engine versions, billing information, troubleshooting, Flink SQL generation, and explicit file output requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and operations teams use this skill to answer Alibaba Cloud Realtime Compute for Flink questions, generate Flink SQL, inspect configuration requirements, and produce file outputs only when explicitly requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may request `aliyun plugin update`, which can change the local CLI plugin environment. <br>
Mitigation: Review and approve that command separately, or skip it unless plugin updates are intended for the current environment. <br>
Risk: Alibaba Cloud account access could expose production or billing data if overly broad credentials are used. <br>
Mitigation: Use a least-privilege RAM account and grant billing or production-wide permissions only when the requested task requires them. <br>
Risk: Static reference files may be outdated for Alibaba Cloud-specific parameters, billing, or engine versions. <br>
Mitigation: Require official Alibaba Cloud documentation retrieval for verified answers and fall back to the documented safe response when evidence is unavailable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-flink-knowledge) <br>
- [Alibaba Cloud Realtime Compute for Apache Flink - Quick Start Guide](references/quickstart.md) <br>
- [Alibaba Cloud Realtime Compute for Apache Flink - Core Concepts](references/concepts.md) <br>
- [Alibaba Cloud Realtime Compute for Apache Flink - SQL Development Reference](references/sql-development.md) <br>
- [Alibaba Cloud Realtime Compute for Apache Flink - Connector Reference](references/connectors.md) <br>
- [Alibaba Cloud Realtime Compute for Apache Flink - Operations Management Reference](references/operations.md) <br>
- [Alibaba Cloud Realtime Compute for Apache Flink - Billing and Engine Versions](references/billing.md) <br>
- [Alibaba Cloud Realtime Compute for Apache Flink - Permissions, Security, and Project Management](references/permissions.md) <br>
- [RAM Policies for alibabacloud-flink-knowledge Skill](references/ram-policies.md) <br>
- [aliyun CLI Configuration Reference](references/aliyun-cli-setup.md) <br>
- [Evaluation Cases](references/evaluation-cases.md) <br>
- [Product Billing](https://help.aliyun.com/zh/flink/realtime-flink/product-overview/billing/) <br>
- [Engine Version Overview](https://help.aliyun.com/zh/flink/realtime-flink/product-overview/engine-version) <br>
- [OpenAPI Reference](https://help.aliyun.com/zh/flink/realtime-flink/developer-reference/openapi-reference/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [File output is permitted only when the user explicitly requests it; otherwise content is delivered inline.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
