## Description:

Generates dual-disease transcriptomic and machine learning research designs for shared biomarkers, hub genes, and mechanisms using public GEO data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External biomedical researchers and developers use this skill to plan comparative transcriptomic studies for two diseases or phenotypes. It helps structure public-GEO study designs covering shared DEGs, PPI and hub-gene analysis, biomarker validation, immune analysis when appropriate, figure planning, and publication upgrades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataset and tool recommendations can become stale as external databases, package availability, and disease-specific GEO suitability change.

Mitigation: Verify GEO dataset suitability, tissue matching, platform compatibility, and package or web-tool availability before running an analysis.

Risk: Generated R examples or workflow steps may not fit a specific disease pair without adjustment.

Mitigation: Review any generated code, replace example accessions and placeholders, validate thresholds, and run feasibility checks before full analysis.

Risk: Biomarker, ROC, hub-gene, and immune-correlation findings can be overinterpreted, especially with small cohorts or inappropriate tissue references.

Mitigation: Require validation cohorts, bootstrap confidence intervals, tissue-appropriate deconvolution tools, and explicit limits on causal or diagnostic claims.

## Reference(s):

- [GEO Dataset Search Strategy and Bioinformatics Tool Reference](references/geo_search_and_tools.md)
- [Tissue Selection and Immune Deconvolution Tool Decisions](references/tissue_and_tool_decisions.md)
- [Figure Plan Template - Dual-Disease Transcriptomic ML Study](references/figure_plan_template.md)
- [Publication Upgrade Path - Dual-Disease Transcriptomic ML Study](references/upgrade_path.md)
- [NCBI Gene Expression Omnibus](https://www.ncbi.nlm.nih.gov/geo/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured study plans and optional R code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Always includes four workload configurations, a recommended primary plan, validation strategy, figure plan, risk review, and publication upgrade path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
