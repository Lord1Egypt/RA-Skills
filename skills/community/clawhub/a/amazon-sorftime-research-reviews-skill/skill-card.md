## Description: <br>
对亚马逊商品评论进行深度分析，自动识别产品痛点、分析退货原因，生成改进建议和客服回复模板。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangdabiao](https://clawhub.ai/user/liangdabiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, product teams, and support teams use this skill to analyze negative Amazon product reviews for a supplied ASIN and marketplace, classify product pain points, and generate actionable improvement suggestions and customer response templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent reads a Sorftime API key and sends the ASIN and marketplace to Sorftime. <br>
Mitigation: Use a dedicated revocable API key and review generated curl commands before execution. <br>
Risk: Raw product and review responses plus generated reports are saved on disk. <br>
Mitigation: Delete raw data files and reports when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liangdabiao/amazon-sorftime-research-reviews-skill) <br>
- [Sorftime MCP documentation](https://sorftime.com/zh-cn/mcp) <br>
- [Pain point taxonomy](references/painpoint_taxonomy.md) <br>
- [Quality issue email templates](assets/email_templates/quality_issue.md) <br>
- [Review analysis design document](设计文档.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Markdown, Guidance] <br>
**Output Format:** [Markdown report, structured JSON analysis, saved raw SSE response files, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local review-analysis report directory containing raw Sorftime responses, negative review analysis JSON, and report.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
