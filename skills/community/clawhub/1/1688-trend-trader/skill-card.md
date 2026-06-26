## Description: <br>
1688 爆款操盘手是一款全栈式供应链 Agent，用于跨境或内贸选品、1688 找工厂、询盘话术生成和利润核算。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skovely](https://clawhub.ai/user/skovely) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External commerce operators, sourcing teams, and agent users use this skill to identify 1688 product opportunities, compare supplier candidates, draft supplier inquiries, calculate margin, and produce a supply-chain execution report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently reuse an ALI_COOKIE value if one is present in the agent environment, causing 1688 requests to run as the logged-in account associated with that cookie. <br>
Mitigation: Do not set ALI_COOKIE unless authenticated 1688 access is intentional; prefer the documented ALI_APP_KEY/ALI_APP_SECRET path or a dedicated low-privilege account. <br>
Risk: Supplier, pricing, certification, and margin outputs may depend on current 1688 page/API data and should not be treated as final procurement approval. <br>
Mitigation: Verify supplier credentials, product certifications, legal restrictions, samples, and logistics assumptions before purchasing or negotiating at scale. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/skovely/1688-trend-trader) <br>
- [1688 Open Platform](https://open.1688.com/) <br>
- [1688 Open API gateway](https://gw.open.1688.com/openapi) <br>
- [选品分析参考](references/selection.md) <br>
- [工厂筛选标准参考](references/sourcing.md) <br>
- [询盘话术模板库](references/inquiry.md) <br>
- [利润核算参考](references/financial.md) <br>
- [供应链落地报告模板](references/report-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Chinese Markdown with tables, supplier comparisons, inquiry templates, margin calculations, and occasional CLI command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May incorporate live or scraped 1688 marketplace data when network access and optional credentials are available.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
