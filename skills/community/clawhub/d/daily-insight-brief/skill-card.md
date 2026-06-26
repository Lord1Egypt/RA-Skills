## Description: <br>
Daily morning brief（8:30 Beijing time）自动收集、交叉验证并提炼来自广域来源的商业、科技、金融等领域信息，产出10-15条要点性简报。每条包含：标题/要点、来源（名称+链接）、关键数据点、分析评论（1-2句）、核心观点、验证状态（已验证 / 待核实）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexweng123](https://clawhub.ai/user/alexweng123) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, analysts, and external users use this skill to generate a structured daily Chinese-language morning brief on business, technology, finance, and market developments. It emphasizes source links, key data points, short analysis, and verification status for each brief item. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring web-based news collection can surface incomplete, stale, or unverified public-source information. <br>
Mitigation: Review each item before relying on it, preserve the skill's verification status field, and mark unsupported claims as pending verification. <br>
Risk: Future integrations could send brief output to Feishu, email, or other channels unintentionally. <br>
Mitigation: Keep external publishing disabled unless the target channel and recipients are intentionally configured and reviewed. <br>
Risk: The artifact includes a stray local-path authoring sentence that is not operational guidance for deployment. <br>
Mitigation: Remove or ignore local authoring paths before release packaging. <br>


## Reference(s): <br>
- [Daily Insight Brief source list](references/source_list.md) <br>
- [ClawHub release page](https://clawhub.ai/alexweng123/daily-insight-brief) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Guidance] <br>
**Output Format:** [Structured Markdown brief with source links, data points, analysis, core insight, and verification status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 10-15 brief items per run; Chinese is the primary language, with optional English notes when useful.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
