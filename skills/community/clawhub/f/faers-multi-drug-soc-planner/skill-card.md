## Description: <br>
Generates FAERS/OpenFDA comparative safety study designs for user-specified drug sets, active comparators, and a single adverse-event SOC or bounded domain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanruoyu](https://clawhub.ai/user/shanruoyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, pharmacovigilance analysts, and developers use this skill to design comparative FAERS/OpenFDA safety studies with workload tiers, active-comparator logic, validation plans, and publication-oriented outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat FAERS disproportionality planning output as medical advice or proof of causality. <br>
Mitigation: Use the output only as research-planning guidance and preserve caveats that FAERS disproportionality is not incidence, risk, or causal evidence. <br>
Risk: Downstream data-analysis code or external tools used to execute the plans may introduce separate security, quality, or reproducibility risks. <br>
Mitigation: Review and scan downstream code, tools, and data-processing pipelines before execution. <br>
Risk: Sparse FAERS fields, underpowered PT counts, multiple comparisons, and drug-name misclassification can produce unstable or misleading study plans. <br>
Mitigation: Apply the skill's data quality gates, drug normalization, active-comparator checks, multiplicity correction, and sensitivity analyses before relying on results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shanruoyu/faers-multi-drug-soc-planner) <br>
- [Publisher profile](https://clawhub.ai/user/shanruoyu) <br>
- [FDA FAERS public dashboard and downloads](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces four workload configurations, a recommended primary plan, workflow steps, figure and table plans, validation strategy, risk review, minimal executable path, and publication upgrade path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
