## Description:

Batch screens multiple resumes against multiple job positions using strict evaluation rules from java-resume-screener skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlin4020](https://clawhub.ai/user/mlin4020)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring teams, and interviewers use this skill to batch screen multiple candidate resumes against one or more job requirements. It extracts resume text, applies hard-requirement checks and weighted scoring, and produces candidate rankings, summaries, and review guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate resume data is extracted and stored locally in text, JSON, and report files.

Mitigation: Use only an approved environment for candidate data, restrict access to generated files, and delete derived resume data when it is no longer needed.

Risk: Untrusted ZIP resume packages may be extracted during resume ingestion.

Mitigation: Avoid untrusted ZIP archives or add extraction limits and path validation before processing archive contents.

Risk: Automated resume screening can produce low-confidence or incomplete evaluations.

Mitigation: Flag low-confidence results for manual review and base conclusions only on resume text and stated job requirements.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, CSV-style tabular data, shell commands, guidance, files]

**Output Format:** [Markdown reports, JSON evaluation files, CSV-style Excel-ready tables, candidate comparison tables, highlights summaries, and shell commands for resume text extraction.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include locally stored resume text, pre-filter JSON, evaluation JSON, ranked reports, confidence scores, and low-confidence manual-review flags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
