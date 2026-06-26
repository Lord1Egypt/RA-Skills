## Description: <br>
Disease CEA Auto helps an agent draft disease-specific pharmacoeconomic analyses by selecting representative therapies, collecting clinical and cost parameters, modeling Markov or decision-tree cost effectiveness, ranking treatments by NMB, and producing Python code plus a scientific report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlb1201](https://clawhub.ai/user/tlb1201) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and health-economics analysts use this skill to prepare China-oriented cost-effectiveness analyses for a specified disease, including model structure, evidence tables, ICER/NMB calculations, sensitivity analysis, charts, Python code, and a bilingual scientific report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical, cost, utility, and GDP inputs are gathered from web sources and may be outdated, incomplete, extrapolated, or inappropriate for the target population. <br>
Mitigation: Verify every cited input against current authoritative sources and have a qualified clinical or health-economics expert review assumptions before relying on outputs. <br>
Risk: Generated ICER, NMB, sensitivity-analysis, and ranking results may be misleading if the model structure or parameters do not match the disease context. <br>
Mitigation: Review the selected Markov, decision-tree, or hybrid model, comparator, time horizon, discounting, and sensitivity-analysis ranges before using the report for policy or commercial decisions. <br>
Risk: The workflow is not intended to process private patient data. <br>
Mitigation: Use only de-identified, aggregate, or public evidence inputs and avoid entering protected health information or other private patient data. <br>


## Reference(s): <br>
- [Model Parameter Reference Guide](artifact/references/model_params.md) <br>
- [ClawHub skill page](https://clawhub.ai/tlb1201/disease-cea-auto) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown report with Python code blocks, tables, citations, and generated chart files when the code is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese/English content; outputs are intended for expert review before decision-making.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
