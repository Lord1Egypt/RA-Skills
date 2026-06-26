## Description: <br>
AssetClaw 资产管理系统 helps agents use AssetHub APIs for asset lifecycle workflows, including asset lookup, repair requests, maintenance work orders, transfers, inventory, depreciation, procurement, retirement, quality control, documents, spare parts, labels, alerts, IoT monitoring, compliance, safety checks, and barcode management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cmu4hlee](https://clawhub.ai/user/cmu4hlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Asset, maintenance, procurement, inventory, compliance, and operations teams use this skill to let an agent query AssetHub data and prepare or execute authenticated asset-management workflows. It is intended for users who have valid AssetHub credentials and appropriate tenant permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad production and administrative authority over AssetHub workflows. <br>
Mitigation: Use a least-privilege AssetHub account and manually confirm admin, restore, delete, approval, and other destructive actions before execution. <br>
Risk: Credential and session handling may expose sensitive AssetHub credentials or tokens through local temporary files. <br>
Mitigation: Avoid storing passwords in the documented /tmp credential file, prefer secure environment handling, and clear token and temporary credential files after use. <br>
Risk: The documented default API URL may use plain HTTP. <br>
Mitigation: Override the API URL to an HTTPS endpoint before using the skill with real credentials or production data. <br>


## Reference(s): <br>
- [AssetClaw ClawHub Listing](https://clawhub.ai/cmu4hlee/assetclaw) <br>
- [AssetClaw Official Site](http://www.medfix.cn) <br>
- [Authentication and Workflow Reference](references/auth-and-workflows.md) <br>
- [AssetHub API Endpoint Quick Reference](references/endpoint-quick-ref.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses authenticated HTTP requests against AssetHub and may cache session state during use.] <br>

## Skill Version(s): <br>
1.5.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
