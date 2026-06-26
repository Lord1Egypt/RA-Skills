## Description: <br>
Generate CIOMS-compliant adverse event narratives for Individual Case Safety Reports (ICSR) from case data for regulatory submission to health authorities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pharmacovigilance and drug-safety teams use this skill to draft standardized adverse event narratives from structured case data. The outputs are drafting aids for ICSR preparation and require qualified medical or pharmacovigilance review before regulatory use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated adverse-event narratives or causality language could be incomplete, medically inaccurate, or unsuitable for regulatory submission without expert review. <br>
Mitigation: Require qualified pharmacovigilance or medical review before using any generated narrative or causality language for submission. <br>
Risk: Case data can contain sensitive patient information. <br>
Mitigation: Use de-identified case data where possible and verify that generated narratives do not include patient identifiers. <br>
Risk: Incorrect input or output file paths could process or overwrite unintended local files. <br>
Mitigation: Keep file paths scoped to the intended case files and review CLI arguments before running the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/AIPOCH-AI/adverse-event-narrative) <br>
- [CIOMS I Guidelines](references/CIOMS_I_Guidelines.md) <br>
- [ICSR Narrative Template](references/ICSR_Template.md) <br>
- [MedDRA Coding Reference](references/MedDRA_Reference.md) <br>
- [Quick Reference Guide](references/Quick_Reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown narrative sections generated from JSON case data, with CLI guidance and validation messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write the generated narrative to a user-specified local output file or print it to stdout.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
