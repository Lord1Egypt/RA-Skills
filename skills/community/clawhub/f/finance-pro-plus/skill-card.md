## Description: <br>
OpenClaw 财务能力终极扩展包 - 覆盖财报分析、杜邦拆解、风险识别、财务报告生成、现金流分析、税务管理等企业级财务工作流。适用于投资分析、尽职调查、财务尽调、预算管理等场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aolikeji](https://clawhub.ai/user/aolikeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance, investment, and diligence users use this skill to guide agents through financial statement analysis, DuPont decomposition, risk identification, valuation modeling, budgeting analysis, tax checks, and finance report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to read local Excel or PDF financial reports that contain confidential budgets, diligence files, tax materials, or non-public financial statements. <br>
Mitigation: Use it only in an environment approved for that data and confirm before allowing the agent to read local files. <br>
Risk: Finance workflows may use web lookups for company, registry, or industry data that can be incomplete, stale, or mismatched to the target entity. <br>
Mitigation: Confirm web lookups before they run and cross-check important financial conclusions against official disclosures, audit reports, or other trusted sources. <br>
Risk: Generated financial analysis, valuation output, or risk ratings could be mistaken for investment advice. <br>
Mitigation: Treat outputs as decision-support material, keep the artifact disclaimer that analysis is for reference only, and require human review before investment, lending, tax, or diligence decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aolikeji/skills/finance-pro-plus) <br>
- [Publisher profile](https://clawhub.ai/user/aolikeji) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown reports and structured finance-analysis guidance, with tables and occasional code or shell-command snippets when the agent needs to process local files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide file reads for Excel or PDF financial reports and web lookups for company or industry data when the user approves those data sources.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
