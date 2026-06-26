## Description: <br>
CMG helps agents scan cloud resources, map them to Tencent Cloud products and specifications, produce TCO analysis from real pricing sources, and guide migration tooling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llm-pm](https://clawhub.ai/user/llm-pm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud migration engineers and solution architects use this skill to inventory resources across Alibaba Cloud, AWS, Huawei Cloud, and GCP, recommend Tencent Cloud equivalents, and prepare pricing-backed TCO reports before migration planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use high-impact cloud credentials for scanning and pricing workflows. <br>
Mitigation: Use temporary least-privilege read-only credentials and avoid main or root account keys. <br>
Risk: The setup workflow can install tools and configure a remote MCP endpoint. <br>
Mitigation: Require operator approval before running setup.sh and review the installed configuration. <br>
Risk: Infrastructure data may be sent to an unverified remote recommendation service. <br>
Mitigation: Replace the default HTTP MCP endpoint with a trusted HTTPS endpoint before using real infrastructure data. <br>
Risk: Downloaded scanner binaries and generated reports may influence migration decisions. <br>
Mitigation: Verify downloaded scanner binaries and review scan, recommendation, and TCO outputs before using them for customer-facing decisions. <br>
Risk: The pricing workflow should not be used with real credentials until TLS verification is fixed. <br>
Mitigation: Block production use of the pricing script with real credentials until certificate verification is restored and retested. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/llm-pm/cmg) <br>
- [CMG resource scan guide](references/scan.md) <br>
- [CMG recommendation guide](references/recommend.md) <br>
- [CMG TCO analysis guide](references/tco.md) <br>
- [CMG migration guide](references/migrate.md) <br>
- [Product code reference](references/products.md) <br>
- [Tencent Cloud pricing calculator](https://buy.cloud.tencent.com/price) <br>
- [Alibaba Cloud pricing calculator](https://www.aliyun.com/price/product) <br>
- [AWS pricing calculator](https://calculator.aws/#/addService) <br>
- [Google Cloud pricing calculator](https://cloud.google.com/products/calculator?hl=zh-CN) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, shell command, Excel, and HTML report references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflows may produce scan spreadsheets, recommendation JSON, pricing data JSON, and TCO reports when the agent runs the bundled scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
