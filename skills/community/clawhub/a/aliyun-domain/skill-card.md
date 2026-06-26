## Description: <br>
Manage Alibaba Cloud domain assets through OpenAPI, including domain queries, renewal, transfer, registration, information changes, promotion consultation, RAG-backed domain guidance, domain monitoring, and creative domain naming. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevin850115](https://clawhub.ai/user/kevin850115) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and domain operators use this skill to inspect and manage Alibaba Cloud domain portfolios, perform domain availability and account queries, prepare domain management actions, monitor expirations and SSL status, and answer domain registration, trading, website-building, and ICP filing questions from bundled reference material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with powerful Alibaba Cloud domain-management authority. <br>
Mitigation: Use a least-privilege Alibaba Cloud RAM key rather than broad account credentials, and review permissions before installation. <br>
Risk: Some live domain-changing examples and methods may not reliably enforce user confirmation. <br>
Mitigation: Require explicit confirmation before transfer, lock, auto-renew, DNS host, registrant, registration, or renewal actions. <br>
Risk: Credential and domain inventory data can expose sensitive account or registrant information. <br>
Mitigation: Avoid permanent shell-profile secrets and redact registrant or domain inventory data before saving reports or sending alerts to email or webhooks. <br>
Risk: The included safe_operation_example.py sample may affect a live account if run with real credentials. <br>
Mitigation: Do not run the sample against a live Alibaba Cloud account unless it has been reviewed and adapted for a controlled environment. <br>


## Reference(s): <br>
- [Aliyun Domain ClawHub release](https://clawhub.ai/kevin850115/aliyun-domain) <br>
- [Alibaba Cloud Domain API Reference](https://next.api.aliyun.com/api/Domain/2018-01-29) <br>
- [Alibaba Cloud Domain Help Documentation](https://help.aliyun.com/product/35836.html) <br>
- [RAG Usage Guide](artifact/scripts/RAG_USAGE_GUIDE.md) <br>
- [Domain Monitoring Guide](artifact/scripts/README_DOMAIN_MONITOR.md) <br>
- [Domain Pricing and Discounts Knowledge Base](artifact/knowledge/domain_pricing_discounts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline command, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Alibaba Cloud API call guidance, domain reports, monitoring recommendations, and user-confirmation prompts for sensitive operations.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
