## Description: <br>
Evaluates how well a candidate resume matches a job description and produces an overall score, dimensional analysis, and interview recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[51mee-com](https://clawhub.ai/user/51mee-com) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Recruiters, hiring teams, and agents supporting hiring workflows use this skill to compare a resume against a job description, rank candidates, and produce a structured match report with interview suggestions. It is intended as decision support, with final hiring decisions reviewed by a person. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Candidate resumes and job descriptions are sent to an external 51mee API. <br>
Mitigation: Use the skill only when authorized to share that data with 51mee, redact unnecessary personal or confidential information where practical, and review the provider's privacy, retention, and compliance terms before use. <br>
Risk: Resume-to-job match scores and recommendations may be incomplete or misleading. <br>
Mitigation: Treat the output as decision support and have qualified hiring staff review the report before interview or rejection decisions. <br>


## Reference(s): <br>
- [51mee Resume Match API endpoint](https://openapi.51mee.com/api/v1/parse/match) <br>
- [ClawHub release page](https://clawhub.ai/51mee-com/51mee-resume-match) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with JSON API response examples and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses multipart/form-data with a resume file and job description; match results should be reviewed before hiring decisions.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
