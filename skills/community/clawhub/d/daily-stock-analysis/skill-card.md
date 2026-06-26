## Description: <br>
Deterministic daily stock analysis skill for global equities. Use when users need daily analysis, next-trading-day close prediction, prior forecast review, rolling accuracy, and reliable markdown report output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HeXavi8](https://clawhub.ai/user/HeXavi8) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to produce repeatable daily equity analysis, next-trading-day close predictions, prior forecast reviews, and rolling accuracy summaries for global stocks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves and reuses local stock-analysis reports in the selected working directory. <br>
Mitigation: Use a dedicated project folder, keep sensitive personal or business data outside that folder, and rely on the skill's working-directory scope controls. <br>
Risk: Legacy report migration can move existing report files after user approval. <br>
Mitigation: Review the listed absolute file paths before approving migration; the documented migration path is explicit and non-destructive. <br>
Risk: Financial predictions and recommendations can be incomplete or incorrect. <br>
Mitigation: Treat outputs as research and informational material, cross-check critical market values with authoritative sources, and do not treat the report as investment advice or a return guarantee. <br>


## Reference(s): <br>
- [Workflow](references/workflow.md) <br>
- [Report Template](references/report_template.md) <br>
- [Metrics Definition](references/metrics.md) <br>
- [Authoritative Information Sources](references/sources.md) <br>
- [Search Query Templates](references/search_queries.md) <br>
- [Minimal Compatibility Mode](references/minimal_mode.md) <br>
- [Security and Privacy Rules](references/security.md) <br>
- [Fundamental Analysis Reference](references/fundamental-analysis.md) <br>
- [Technical Analysis Reference](references/technical-analysis.md) <br>
- [Financial Metrics Reference](references/financial-metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report files with YAML frontmatter, structured tables, script command usage, and concise run summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved under the configured working directory with versioned filenames; history reads are capped and prior predictions are reused for rolling accuracy.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
