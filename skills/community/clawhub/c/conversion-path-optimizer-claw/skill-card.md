## Description: <br>
转化路径优化虾 analyzes sales funnels, mines high-converting sales scripts, and recommends optimization actions for sales teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales operations, revenue operations, and sales enablement teams use this skill to analyze funnel conversion rates, find drop-off points, extract effective sales scripts from CRM or conversation records, and prepare recommendations or training materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CRM exports and sales conversations can contain sensitive customer or business data. <br>
Mitigation: Use explicit local input and output paths, remove customer identifiers where practical, and review generated reports before sharing. <br>
Risk: Creating a Feishu document may send selected analysis content to the configured Feishu account. <br>
Mitigation: Only request Feishu document creation after confirming what data will be included and which account or token will be used. <br>
Risk: Sales script recommendations are based on observed statistical patterns and may not generalize to every customer segment. <br>
Mitigation: Validate recommendations with current sales context and use A/B testing or human review before broad rollout. <br>


## Reference(s): <br>
- [销售漏斗建模指南](references/funnel-modeling.md) <br>
- [行业话术模板库](references/industry-templates.md) <br>
- [话术效果评估框架](references/script-evaluation.md) <br>
- [话术挖掘算法库](references/script-mining.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown reports, ranked recommendation lists, script manuals, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local HTML reports or request creation of a Feishu document when the user asks for that output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
