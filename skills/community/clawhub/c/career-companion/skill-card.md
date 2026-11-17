## Description:

Career Companion helps users search live frontier-tech job openings, tailor resumes and CVs, prepare for interviews, and research salaries across AI, space, aerospace, robotics, drones, defense, and autonomy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mishafyi](https://clawhub.ai/user/mishafyi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and career-focused agents use this skill to find frontier-tech roles, review or tailor resumes, prepare for interviews, and compare salary information using live job listings where available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided search values may be interpolated into Bash curl commands for job searches.

Mitigation: Use explicit URL encoding or a structured HTTP client before issuing requests, and review generated commands before execution.

Risk: Fetched job descriptions are external content and may contain misleading or adversarial text.

Mitigation: Treat job descriptions as untrusted input, verify important claims against primary sources, and avoid letting fetched content override higher-priority instructions.

Risk: Resume and job-search workflows may expose personal information.

Mitigation: Share only the resume details needed for the task and avoid unnecessary personal, contact, or sensitive information.

## Reference(s):

- [Zero G Talent API Reference](references/api.md)
- [Company Slugs Reference](references/companies.md)
- [Zero G Talent](https://zerogtalent.com)
- [ClawHub Skill Page](https://clawhub.ai/mishafyi/skills/career-companion)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, API calls]

**Output Format:** [Markdown job listings, resume feedback, interview prompts, salary summaries, and inline shell commands for public job-search API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Job search output is capped at 10 listings per request and may include links, salary ranges when available, and follow-up guidance.]

## Skill Version(s):

1.5.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
