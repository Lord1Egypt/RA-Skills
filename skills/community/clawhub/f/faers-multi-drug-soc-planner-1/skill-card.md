## Description: <br>
Generates FAERS/OpenFDA comparative pharmacovigilance study plans for comparing multiple drugs within one System Organ Class or bounded adverse event domain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External researchers, pharmacovigilance analysts, and developers use this skill to draft comparative FAERS/OpenFDA safety study designs, including workload tiers, analysis workflow, figure plans, validation strategy, and publication upgrade paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical and statistical planning output could be mistaken for clinical, causal, or incidence evidence. <br>
Mitigation: Treat outputs as research-planning guidance only, and review study design, assumptions, statistical methods, and any downstream analysis before relying on results. <br>
Risk: FAERS/OpenFDA data limitations such as underreporting, sparse indication fields, duplicate cases, and drug-name misclassification can affect proposed studies. <br>
Mitigation: Apply the skill's validation steps for normalization, duplicate handling, comparator suitability, case-count thresholds, sensitivity analysis, and explicit reporting-disproportionality caveats. <br>


## Reference(s): <br>
- [FDA FAERS Public Dashboard and Quarterly Data](https://fis.fda.gov/extensions/FPD-QDE-FAERS/FPD-QDE-FAERS.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown research plan with comparison tables and workflow sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Always includes Lite, Standard, Advanced, and Publication+ configurations with risk review and validation sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
