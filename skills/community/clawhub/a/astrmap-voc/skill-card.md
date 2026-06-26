## Description: <br>
星图AI·客户洞察（VOC），帮助全球电商卖家进行产品改进、新品开发、市场调研！核心能力：获取亚马逊评论、AI深度分析差评、精准量化高频问题、挖掘高星隐性差评、生成改进建议、追踪评论趋势、增量更新。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sparkbayes](https://clawhub.ai/user/sparkbayes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers and developers use this skill to collect Amazon review data through AstrMap, retrieve completed analysis, and guide review trend, sentiment, issue, and product-improvement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends CUSTOMER_INSIGHTS_API_KEY to AstrMap for authenticated API calls. <br>
Mitigation: Install only if you trust AstrMap, pass the key through the configured environment variable or command argument, and rotate or disable the key when it is no longer needed. <br>
Risk: Collection workflows can require an AstrMap desktop client connected to an Amazon buyer account. <br>
Mitigation: Use a dedicated Amazon buyer account for collection, keep it separate from business-critical seller accounts, and use result-only workflows when desktop collection is not required. <br>
Risk: Desktop client downloads and execution introduce local software trust risk. <br>
Mitigation: Use AstrMap-provided download links, verify HTTPS, checksum or integrity data when available, and platform code signing before running the client. <br>
Risk: Task creation, incremental collection, and analysis actions can spend account credits. <br>
Mitigation: Check available points and obtain explicit user confirmation before actions that consume credits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sparkbayes/astrmap-voc) <br>
- [AstrMap API reference](artifact/references/api_reference.md) <br>
- [AstrMap desktop client security guide](artifact/references/security.md) <br>
- [AstrMap website](https://www.astrmap.com/) <br>
- [AstrMap download configuration](https://www.astrmap.com/download-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CUSTOMER_INSIGHTS_API_KEY for authenticated actions; some collection workflows require the AstrMap desktop client.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
