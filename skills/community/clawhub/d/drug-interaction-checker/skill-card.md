## Description: <br>
Checks drug-drug interactions across multiple medications and reports severity, mechanisms, effects, recommendations, summaries, and warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to screen medication lists for known or class-based drug interaction signals before confirming any concern with a pharmacist or clinician. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce specific medication-change guidance that may be mistaken for medical advice. <br>
Mitigation: Treat results as educational screening only and confirm interaction concerns with a pharmacist or clinician before changing, stopping, starting, or combining medications. <br>
Risk: The local interaction data may be incomplete or not account for patient-specific factors. <br>
Mitigation: Use the output as a prompt for professional review, especially for renal or hepatic impairment, pregnancy, age-related risk, comorbidities, and complex medication lists. <br>
Risk: The installation path includes a pip dependency step. <br>
Mitigation: Install and run the skill in a virtual environment before use. <br>


## Reference(s): <br>
- [Drug Interaction Checker ClawHub release](https://clawhub.ai/AIPOCH-AI/drug-interaction-checker) <br>
- [interactions_db.json](artifact/references/interactions_db.json) <br>
- [cyp450_substrates.json](artifact/references/cyp450_substrates.json) <br>
- [Drug Interaction Severity Classification Criteria](artifact/references/severity_criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, markdown, code, shell commands, guidance] <br>
**Output Format:** [Text or JSON interaction reports; documentation also describes markdown output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports checked drugs, pairwise interactions, severity counts, warnings, mechanisms, effects, and recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
