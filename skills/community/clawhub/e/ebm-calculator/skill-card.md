## Description: <br>
Evidence-Based Medicine calculator for sensitivity, specificity, PPV, NPV, NNT, and likelihood ratios for clinical decision making and biostatistics education. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, clinicians, educators, and developers use this skill to run local evidence-based medicine calculations for diagnostic accuracy, likelihood ratios, number needed to treat, and pre-test to post-test probability changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional output path can overwrite a user-selected file. <br>
Mitigation: Prefer stdout, or choose an output path inside the workspace and confirm it is safe to write before execution. <br>
Risk: Medical-statistics outputs can be misused as standalone clinical advice. <br>
Mitigation: Treat outputs as educational or decision-support calculations and have qualified clinical judgment verify the inputs and conclusions. <br>


## Reference(s): <br>
- [EBM Calculator References](artifact/references/guidelines.md) <br>
- [ClawHub Skill Release](https://clawhub.ai/AIPOCH-AI/ebm-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON results with optional Markdown command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are printed to stdout by default and can optionally be written to a user-selected output file.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
