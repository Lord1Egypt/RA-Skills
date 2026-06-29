## Description: <br>
招中标数据智能体-AI驱动的标讯分析Agent helps AI agents search Chinese tender and award notices, retrieve bid details, analyze companies and markets, and produce structured procurement intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External AI-agent users and developers use this skill to query bid notices, inspect company procurement activity, compare suppliers and competitors, analyze market trends, and generate structured reports or dashboard-ready data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may contact the vendor service and transmit local device or user identifiers during automatic registration. <br>
Mitigation: Prefer a manually configured API key and require explicit user confirmation before registration or any transmission of device or user identifiers. <br>
Risk: The skill may store a vendor API key locally after automatic registration. <br>
Mitigation: Review the target configuration path and credential contents before persistence, restrict file permissions, and avoid automatic credential storage in shared or managed environments. <br>
Risk: The security scan reports suspicious behavior around account creation, credential persistence, and recharge or login-link flows. <br>
Mitigation: Require explicit confirmation before contact lookup, registration, credential persistence, recharge guidance, or login-link generation, and install only where vendor-service use is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhiliaobiaoxun/skills/bid-data-intelligent-agent) <br>
- [Bid search API reference](artifact/references/api-search.md) <br>
- [Company analysis API reference](artifact/references/api-company.md) <br>
- [Market analysis API reference](artifact/references/api-market.md) <br>
- [Automatic registration flow](artifact/references/auto-register.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and API request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can call vendor APIs, persist an API key in local configuration when auto-registering, and return procurement, company, and market analysis.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
