## Description:

Use when the user shares a job description and asks which keywords or skills to put on their resume, whether their resume will pass an ATS (applicant tracking system), or what a resume is missing for a specific job. Free, no-auth keyword extraction with an optional resume coverage check.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a0971025732-netizen](https://clawhub.ai/user/a0971025732-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External job seekers use this skill to identify ranked keywords and experience requirements in a job description, then optionally compare those keywords with resume text. It reports missing terms for the user to assess without inventing qualifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example automatically sends a local resume.txt file to an external service when it is present, and the cited documentation does not establish resume-data retention guarantees.

Mitigation: Use a dedicated folder containing only documents intended for sharing. Omit resume.txt unless comparison is wanted, remove contact details before sending, and check the service's retention practices first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a0971025732-netizen/skills/ats-keyword-extractor)
- [Keyword extraction MCP endpoint](https://finch-agent-catalog.finch-catalog-mcp.workers.dev/mcp)
- [Public repository documentation](https://github.com/a0971025732-netizen/finch-agent-catalog-mcp)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured JSON keyword analysis summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked keywords, mentions, and job-description sections; may include experience requirements and, when resume text is provided, coverage and missing keywords. Heuristic extraction works best with English job descriptions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
