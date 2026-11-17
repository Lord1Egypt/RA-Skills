## Description:

Gaokao Volunteer helps agents guide Chinese Gaokao applicants through score and rank matching, university recommendations, reach/match/safety planning, and province-specific application checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and education-planning agents use this skill to collect Gaokao applicant details, search current admissions data, classify options into reach/match/safety tiers, and produce advisory application plans. The skill is intended for Chinese college application planning and should be used with official admissions sources.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Generated HTML reports can include unescaped imported data, so reports built from untrusted sources could display or run unwanted content.

Mitigation: Review the skill before installation, use official admissions data where possible, avoid untrusted JSON or scraped content, and treat generated reports as advisory before opening or sharing them.

Risk: Admissions scores, ranks, and provincial rules change yearly, which can make recommendations stale or misleading.

Mitigation: Verify batch lines, one-score-one-rank tables, and admissions data against official provincial education examination sources before making application decisions.

Risk: The skill processes visible score, rank, preference, and application-plan details in reports.

Mitigation: Avoid storing sensitive applicant details longer than needed and review generated HTML before sharing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bettermen/skills/gaokao-volunteer)
- [Source repository](https://github.com/bettermen/gaokao-volunteer)
- [Province rules](references/province_rules.json)
- [University basics](references/university_basics.json)
- [Major catalog](references/major_catalog.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Conversational guidance, JSON intermediate data, shell commands, and generated HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current admissions data supplied through search or user input; generated plans are advisory and require official-source verification.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
