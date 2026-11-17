## Description:

连接和分析聚水潭 ERP 数据，帮助商家保存本地连接资料，并按自然语言编排店铺授权、商品、库存、订单、采购、日报和补货提醒等经营分析场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and operations teams use this skill to connect Jushuitan ERP credentials, confirm data consent, query ERP data, and turn shop authorization, product, inventory, order, return, purchasing, replenishment, and daily reporting questions into business-facing analysis or rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive Jushuitan ERP credentials locally and uses them for authenticated API calls.

Mitigation: Use least-privileged, read-only ERP tokens where possible, avoid passing secrets in shell commands or logs, restrict file permissions for local credential profiles, and rotate credentials if exposure is suspected.

Risk: The scanner notes that consent and endpoint limits are not enforced in code.

Mitigation: Confirm user consent before each real data access, request only the ERP permissions needed for the current workflow, review profiles.json handling before deployment, and prefer or add an endpoint allowlist for production use.

## Reference(s):

- [聚水潭 ERP 接口使用方法](references/api-map.md)
- [聚水潭 ERP 场景手册](references/scenarios.md)
- [聚水潭开放平台](https://openweb.jushuitan.com/)
- [聚水潭开放平台应用管理](https://openweb.jushuitan.com/management/apps)
- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-shop-jushuitan-erp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON snippets with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local profiles.json and consent.json files, and may call Jushuitan ERP APIs when credentials, permissions, and consent are present.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
