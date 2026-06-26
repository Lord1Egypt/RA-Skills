## Description: <br>
Batch screens multiple resumes against multiple job positions using strict evaluation rules from java-resume-screener skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mlin4020](https://clawhub.ai/user/mlin4020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring teams, and technical interviewers use this skill to batch screen multiple candidate resumes against one or more job requirements. It extracts resume text, applies hard requirement checks and weighted scoring, then produces ranked reports and review data for human hiring decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The resume extraction step may process more local PDF files than intended if run against a broad or mixed directory. <br>
Mitigation: Run the skill only in a dedicated folder containing the specific resumes intended for screening. <br>
Risk: ZIP extraction and generated intermediate files can expose confidential candidate data or retain it longer than expected. <br>
Mitigation: Use trusted ZIP files, treat generated text, JSON, CSV, and Markdown outputs as confidential, and delete intermediate files after review. <br>
Risk: Automated resume scoring can produce incorrect or incomplete screening conclusions. <br>
Mitigation: Use confidence scores and low-confidence flags to route results through human recruiter or interviewer review before hiring decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mlin4020/batch-resume-screener) <br>
- [Publisher Profile](https://clawhub.ai/user/mlin4020) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON evaluation files, Excel-ready tabular text, comparison tables, highlights summaries, and extracted resume text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes resume files in batches, includes confidence scores, and flags low-confidence evaluations for manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
