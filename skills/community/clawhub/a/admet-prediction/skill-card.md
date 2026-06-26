## Description: <br>
ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) prediction for drug candidates to assess drug-likeness, pharmacokinetic properties, and safety risks early in drug discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huifer](https://clawhub.ai/user/huifer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, researchers, and drug discovery teams use this skill to screen compounds for ADMET properties, drug-likeness, pharmacokinetic concerns, and toxicity signals before prioritizing candidates for experimental follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ADMET, PK, hERG, DILI, Ames, and progression recommendations are screening predictions rather than experimental evidence. <br>
Mitigation: Validate important safety and development decisions experimentally before using results for candidate progression. <br>
Risk: Running local analysis on unintended compound libraries could expose or process data outside the user's intended scope. <br>
Mitigation: Install dependencies in a virtual environment and run the tool only on compound files selected for analysis. <br>


## Reference(s): <br>
- [ADMET Properties Reference](reference/admet-properties.md) <br>
- [Toxicity Alerts Reference](reference/toxicity-alerts.md) <br>
- [ClawHub skill page](https://clawhub.ai/huifer/admet-prediction) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown summaries and JSON result files for single-compound, batch, and filtering workflows.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include ADMET property tables, rule-filter results, confidence-oriented interpretation, and recommendations for experimental validation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
