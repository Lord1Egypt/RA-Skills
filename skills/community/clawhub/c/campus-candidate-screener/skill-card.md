## Description: <br>
Screens campus recruiting candidates against role requirements and produces explainable shortlists with candidate details, match scores, recommendation levels, and review reasons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linuoxu](https://clawhub.ai/user/linuoxu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR teams and hiring reviewers use this skill to screen campus recruiting candidates against job responsibilities, education and major requirements, skills, and hiring constraints. It helps produce reviewable candidate rankings, recommendation levels, rejection or follow-up reasons, and next-step guidance for interview outreach or manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated shortlists may expose candidate contact details and other sensitive personal information if shared too broadly. <br>
Mitigation: Install only for authorized recruiting use, restrict outputs to HR or hiring reviewers, and ask the agent to mask phone numbers or email addresses unless full details are needed for outreach. <br>
Risk: Candidate ranking could reflect non-job-related or sensitive attributes if those are included in the input. <br>
Mitigation: Use only role-related criteria such as education requirements, major, skills, projects, internships, certificates, language ability, and job responsibility match; route uncertain cases to human review. <br>
Risk: Incomplete candidate information may be mistaken for a poor match. <br>
Mitigation: Mark missing fields as not provided and classify potentially qualified candidates with missing evidence for follow-up or manual review rather than automatic rejection. <br>


## Reference(s): <br>
- [Campus Candidate Screener release page](https://clawhub.ai/linuoxu/campus-candidate-screener) <br>
- [Campus candidate scoring rubric](references/scoring-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown tables and concise narrative recommendations, typically in Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes role requirement parsing, candidate summaries, scores, recommendation levels, review reasons, missing-information flags, and HR next-step guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
