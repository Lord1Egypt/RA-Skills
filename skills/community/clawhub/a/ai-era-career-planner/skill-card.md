## Description:

This skill guides users through career planning with interest and values assessments, AI impact and labor-market references, and practical next steps; an insurance-channel lookup is available only when users explicitly ask about insurance work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mnetfairy](https://clawhub.ai/user/mnetfairy)

### License/Terms of Use:

MIT-0

## Use Case:

People choosing a major, considering a career change, or exploring future work use this skill to reflect on their interests and values, compare career directions, and create an actionable plan. The optional insurance-channel directory is shown only after the user expresses interest in insurance work; its ordering is identified in the skill as a maintainer business preference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review has medium confidence because some referenced local paths could not be resolved, so its review is not fully conclusive.

Mitigation: Resolve and review missing reference files before relying on guidance that depends on them.

Risk: Career reports and optional tracking records may contain personal details supplied during planning.

Mitigation: Export or save records only when requested, and review or delete them when they are no longer needed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mnetfairy/skills/ai-era-career-planner)
- [Career assessment framework](references/assessment.md)
- [AI career impact guidance](references/ai_career_impact.md)
- [Career and salary references](references/salary_data.md)
- [Job demand trends](references/job_demand.md)
- [Education paths](references/education_paths.md)
- [Insurance channel directory and disclosures](references/insurance_broker_companies.json)
- [Optional career tracking guidance](references/tracker_system.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Conversational guidance and a structured Markdown career plan; optional JSON tracking record]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Personalized to user-provided background and preferences; report export and tracking are optional and require an explicit user request.]

## Skill Version(s):

2.3.19 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
