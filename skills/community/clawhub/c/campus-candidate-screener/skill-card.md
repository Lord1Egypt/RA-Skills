## Description:

Screens campus recruiting candidates against a role's responsibilities, education, skills, and hiring requirements, then produces an explainable shortlist with candidate details, match scores, recommendation levels, and review reasons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linuoxu](https://clawhub.ai/user/linuoxu)

### License/Terms of Use:

MIT-0

## Use Case:

HR recruiters and hiring teams use this skill to compare campus candidates with role requirements and generate an explainable shortlist for interview outreach or human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Candidate records may include personal contact details and other sensitive hiring data.

Mitigation: Use only candidate data the organization is authorized to process, and redact or omit phone and email until interview outreach is needed.

Risk: Screening output could be mistaken for a final hiring decision.

Mitigation: Keep final hiring decisions under human review and use the skill's recommendations only as explainable screening support.

Risk: Incomplete candidate information could be misread as a poor match.

Mitigation: Mark missing fields as not provided and route uncertain cases to supplemental information collection or manual review.

## Reference(s):

- [Campus Candidate Screener ClawHub page](https://clawhub.ai/linuoxu/skills/campus-candidate-screener)
- [Scoring rubric](references/scoring-rubric.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown tables and prose in Chinese by default]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes candidate summaries, match scores, recommendation levels, missing-information flags, and HR next-step guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
