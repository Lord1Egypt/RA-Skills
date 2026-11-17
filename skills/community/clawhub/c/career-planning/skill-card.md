## Description:

Chinese-language career-planning agent skill that routes job-search requests across career planning, job description analysis, resume optimization, interview preparation, application planning, and HR or compensation communication workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moly-yan](https://clawhub.ai/user/moly-yan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to produce structured Chinese-language job-search guidance, including career plans, JD analysis cards, resume improvement reports, interview preparation cards, application plans, and HR or salary negotiation guidance. It is designed around China-based recruiting scenarios while allowing user-provided profile details to override its defaults.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Users may share sensitive resume, salary, ID, banking, or address details while seeking job-search guidance.

Mitigation: Ask users to omit unnecessary sensitive data, prefer ranges for compensation and location details, and remove unrelated identity or financial fields before analysis.

Risk: Career, salary, offer, legal, and market guidance can become stale or be over-applied to individual decisions.

Mitigation: Require source and time labels for market claims, mark missing facts as assumptions, and direct users to independently verify live salary, legal, offer, and market information.

Risk: Resume and interview assistance could encourage exaggerated or fabricated claims if used carelessly.

Mitigation: Keep recommendations tied to user-provided evidence, use placeholders for missing achievements, and avoid fabricating experience, credentials, offers, salary documents, or background-check narratives.

## Reference(s):

- [Skill Definition](artifact/SKILL.md)
- [Usage Guide](artifact/USAGE.md)
- [Default Profile and Domain Knowledge](artifact/references/default-profile.md)
- [Career Planning Module](artifact/references/module-career.md)
- [Job Analysis Module](artifact/references/module-job-analysis.md)
- [Resume Optimization Module](artifact/references/module-resume.md)
- [Interview Preparation Module](artifact/references/module-interview.md)
- [Application Planning Module](artifact/references/module-apply.md)
- [HR and Compensation Module](artifact/references/module-hr.md)
- [Framework Templates](artifact/references/frameworks.md)
- [Boundary Examples](artifact/references/example-boundary.md)
- [Deep FAQ](artifact/references/faq-deep.md)
- [ClawHub Skill Page](https://clawhub.ai/moly-yan/skills/career-planning)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style structured reports, cards, tables, checklists, and scripts for user review]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include default-profile assumptions and live-data caveats when user inputs or current market data are missing.]

## Skill Version(s):

1.6.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
