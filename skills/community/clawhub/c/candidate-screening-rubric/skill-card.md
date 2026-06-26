## Description: <br>
Screens candidate materials against a job description with evidence-cited scoring, bias checks, and a draft Advance/Hold/Decline verdict with targeted follow-up questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring managers, and talent partners use this skill to turn a job description and candidate materials into a structured screening rubric that can be reviewed by a hiring team and attached to a candidate record. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate materials may include direct identifiers or protected-characteristic signals that could bias screening or be stored unnecessarily. <br>
Mitigation: Redact names, emails, phone numbers, exact addresses, photos, and other direct identifiers where possible, and score only cited job-related evidence. <br>
Risk: A draft rubric verdict could be mistaken for an automated hiring decision. <br>
Mitigation: Treat outputs as structured aids for human review; final decisions should use panel calibration and structured interviews based on the cited gaps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/candidate-screening-rubric) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown screening rubric with tables, cited evidence, verdict rationale, and structured next-round questions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft screening aid for human hiring-team review; it does not execute code or take external actions.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata and CHANGELOG, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
