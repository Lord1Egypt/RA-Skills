## Description: <br>
Generates hospital discharge summaries from structured admission data, hospital course details, medications, and follow-up plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical documentation teams and clinicians can use this skill to draft discharge summaries from structured inpatient records before physician review and institutional compliance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated summaries may contain inaccurate diagnoses, medication details, dates, follow-up instructions, or language. <br>
Mitigation: Treat generated summaries as drafts and verify all clinical content with a qualified clinician before use. <br>
Risk: Patient data may be handled in local input and output files. <br>
Mitigation: Install and run the skill only in environments approved for patient data and choose output paths carefully. <br>
Risk: The script writes to the selected output path and can overwrite an existing file. <br>
Mitigation: Review output paths before execution and keep backups or versioned destinations for clinical drafts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AIPOCH-AI/discharge-summary-writer) <br>
- [Standard Discharge Summary Template](references/discharge_template.md) <br>
- [Medical Terms](references/medical_terms.json) <br>
- [Section Writing Guidelines](references/section_guidelines.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown or JSON discharge-summary documents written to a local file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports standard, structured, and JSON output formats with zh/en language options.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
