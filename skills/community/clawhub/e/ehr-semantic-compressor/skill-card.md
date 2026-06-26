## Description: <br>
Summarizes lengthy Electronic Health Record documents into structured summaries and extracted clinical sections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and clinical operations teams can use this skill to compress long EHR text into reviewable summaries and extracted sections such as allergies, medications, diagnoses, family history, procedures, and vitals. Human clinical review is required before relying on the output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical summaries may be inaccurate, incomplete, or misleading for patient care decisions. <br>
Mitigation: Require qualified human review of every summary and validate the tool against approved clinical evaluation data before operational use. <br>
Risk: The artifact claims Transformer-based clinical AI behavior that the implementation and security summary do not validate. <br>
Mitigation: Do not rely on the Transformer or clinical-accuracy claims unless the implementation is replaced or independently validated. <br>
Risk: The root requirements file lists an unexpected 'main' package for a sensitive medical-data workflow. <br>
Mitigation: Inspect dependency files before installation and avoid installing the unexpected package without provenance checks. <br>
Risk: The skill processes EHR content and can write summary files containing PHI. <br>
Mitigation: Run only in a secure PHI-approved workspace, restrict input and output paths, and de-identify data where policy requires it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AIPOCH-AI/ehr-semantic-compressor) <br>
- [Clinical Summarization Guidelines](references/guidelines.md) <br>
- [Sample Input](references/sample_input.json) <br>
- [Sample Output](references/sample_output.json) <br>
- [Python Dependencies](references/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration] <br>
**Output Format:** [JSON by default, with Markdown and plain text options described by the artifact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write output to a file or stdout; summary length and extracted clinical sections are configurable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
