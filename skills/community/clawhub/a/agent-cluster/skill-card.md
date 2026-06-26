## Description: <br>
Agent Cluster is a multi-agent business automation framework for B2B e-commerce, CMS, Amazon, and ERP workflows with specialist agents for inventory, procurement, finance, logistics, approvals, and engine routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business-operations teams use this skill to coordinate multi-agent workflows across CMS, ERP, Amazon, inventory, procurement, finance, and logistics systems. It is intended for automation scenarios that require connector configuration, approval gates, audit logging, and least-privilege credential handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package can require ERP, CMS, Amazon, model-provider, and other sensitive credentials while supporting live commerce or business-system operations. <br>
Mitigation: Review the full scope with an administrator, use separate least-privilege credentials, and keep live write or delete operations disabled until permissions, approval gates, and connectors are verified. <br>
Risk: Local logs, memory, and snapshots may retain sensitive operational or customer data. <br>
Mitigation: Store generated data only in approved locations, verify redaction behavior, restrict file access, and set retention limits before production use. <br>
Risk: The public CMS-focused summary understates the broader enterprise automation, marketing, security-audit, and customer-service capabilities present in the artifact. <br>
Mitigation: Perform an administrator review of enabled modules and disable unneeded capabilities before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/agent-cluster) <br>
- [Project Homepage](https://github.com/WangM-A3/agent-cluster) <br>
- [README](README.md) <br>
- [Security Statement](SECURITY.md) <br>
- [Pricing](PRICING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, Python code, YAML/JSON configuration, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require ERP, CMS, Amazon, Anthropic, and DeepSeek credentials depending on enabled connectors and execution engines.] <br>

## Skill Version(s): <br>
3.0.4 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
