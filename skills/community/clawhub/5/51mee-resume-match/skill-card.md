## Description:

Matches resumes to job descriptions to assess candidate-role fit and help rank candidates for a position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[51mee-com](https://clawhub.ai/user/51mee-com)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters and hiring teams use this skill to compare candidate resumes with job descriptions, generate match scores across skills, experience, education, and salary, and produce interview suggestions or batch ranking summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate resumes and job descriptions are sent to the third-party API at openapi.51mee.com.

Mitigation: Confirm candidate and organizational permission, remove unnecessary personal details where possible, and verify the provider's privacy, retention, deletion, and compliance terms before use.

Risk: Automated match scores and recommendations could be over-relied on in hiring decisions.

Mitigation: Use the report as decision support and require human review before making candidate screening or interview decisions.

## Reference(s):

- [51mee resume match API endpoint](https://openapi.51mee.com/api/v1/parse/match)
- [ClawHub skill page](https://clawhub.ai/51mee-com/skills/51mee-resume-match)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Analysis, Guidance]

**Output Format:** [Markdown report with structured score tables, fit analysis, gaps, interview suggestions, and recommendation text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a resume file and job description text; check the API response code before using the returned analysis.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
