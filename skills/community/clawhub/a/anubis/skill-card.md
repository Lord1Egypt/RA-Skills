## Description: <br>
Anubis Standard is a career application engine that rewrites a resume and creates a tailored cover letter for a specific job, with ATS keyword optimization and file outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[occupythemilkyway](https://clawhub.ai/user/occupythemilkyway) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job applicants and career-support agents use this skill to tailor a resume and cover letter to a job description while preserving the candidate's stated facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill prints full resume and job-description contents to console output, which may expose sensitive personal or application information in transcripts or logs. <br>
Mitigation: Run only in trusted environments, avoid shared or hosted sessions for sensitive applications, and review transcript and logging behavior before use. <br>
Risk: The skill writes generated application documents to a local output directory and may overwrite or commingle files with same-date names. <br>
Mitigation: Choose OUTPUT_DIR deliberately and check for existing same-date files before saving generated documents. <br>
Risk: Generated resume and cover-letter content could overstate qualifications if not reviewed against the source resume. <br>
Mitigation: Review all generated documents before submission and remove any claim that is not supported by the candidate's actual experience. <br>


## Reference(s): <br>
- [Anubis ClawHub listing](https://clawhub.ai/occupythemilkyway/anubis) <br>
- [occupythemilkyway publisher profile](https://clawhub.ai/user/occupythemilkyway) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown documents and console guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a tailored resume and cover letter to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
