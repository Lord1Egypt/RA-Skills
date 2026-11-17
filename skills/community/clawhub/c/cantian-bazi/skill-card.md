## Description:

Provides Bazi/Four Pillars charting, Chinese almanac lookup, true-solar-time conversion, and decade, annual, monthly, daily, and hourly fortune-cycle range queries for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianlinle](https://clawhub.ai/user/tianlinle)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to answer Bazi/Four Pillars, solar and lunar calendar, huangli, true-solar-time, and fortune-cycle range questions by running local TypeScript scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing npm dependencies can execute third-party code during install or runtime.

Mitigation: Install only in a restricted project directory after reviewing the dependency set.

Risk: The cantian-tymext dependency is declared as a version range.

Mitigation: Pin cantian-tymext to an exact reviewed version and add a package-lock.json before deployment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tianlinle/skills/cantian-bazi)
- [Publisher profile](https://clawhub.ai/user/tianlinle)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown reports and plain text strings from local TypeScript commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fortune range outputs expand by requested level; hourly queries are limited to ranges of 62 days or less.]

## Skill Version(s):

0.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
