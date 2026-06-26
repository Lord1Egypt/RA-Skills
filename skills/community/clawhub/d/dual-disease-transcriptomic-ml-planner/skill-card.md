## Description: <br>
Generates complete dual-disease transcriptomic and machine learning research designs from a user-provided disease pair for shared DEGs, common hub genes, cross-disease biomarkers, and shared molecular mechanisms using public GEO data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers and biomedical data analysts use this skill to plan GEO-based comparative transcriptomic studies for two diseases, including workload options, analysis workflow, figure plan, validation strategy, and publication upgrade path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated plans may be followed with package installation or external web services during downstream analysis. <br>
Mitigation: Install R packages only from trusted repositories and avoid sending confidential or non-public data to external services. <br>
Risk: Biomedical study plans can overstate biomarker, immune-correlation, or mechanistic claims when cohorts are small or poorly matched. <br>
Mitigation: Review the generated plan before use, require validation cohorts where feasible, report uncertainty such as bootstrap confidence intervals, and keep association findings distinct from causal claims. <br>


## Reference(s): <br>
- [GEO Dataset Search Strategy and Bioinformatics Tool Reference](references/geo_search_and_tools.md) <br>
- [Tissue Selection and Immune Deconvolution Tool Decisions](references/tissue_and_tool_decisions.md) <br>
- [Figure Plan Template - Dual-Disease Transcriptomic ML Study](references/figure_plan_template.md) <br>
- [Publication Upgrade Path - Dual-Disease Transcriptomic ML Study](references/upgrade_path.md) <br>
- [NCBI Gene Expression Omnibus](https://www.ncbi.nlm.nih.gov/geo/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with tables, step-by-step plans, R code examples, and command or package guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Always produces four workload configurations plus a recommended plan, validation strategy, figure plan, minimal executable version, and publication upgrade path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
