## Description:

Summarizes competitors’ newly published and granted patents by technical direction, highlights noteworthy items, and delivers a concise brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Business and technology teams use this skill to review a competitor’s newly published and granted patents over a chosen period, identify technical themes, and prepare a brief for follow-up. It is not an infringement assessment or an automatic monitoring service.

### Deployment Geography for Use:

Global; patent coverage depends on the selected jurisdiction and available database coverage.

## Known Risks and Mitigations:

Risk: The security assessment warns that weaknesses could expose API credentials.

Mitigation: Before using a paid key, confirm its destination; use a limited trial key where possible and do not paste secrets into chat.

Risk: The security assessment warns that cache-path validation weaknesses could write files outside the intended cache.

Mitigation: Use a controlled cache/output location and verify the destination before running the skill.

Risk: Patent searches can incur charges, and unexpectedly empty statistics may need review.

Mitigation: Submit only approved search terms, set a spending limit, and verify unexpectedly empty statistics.

## Reference(s):

- [ClawHub release](https://clawhub.ai/ip930/skills/competitor-patent-brief)
- [PatentMax](https://ip930.com)
- [PatentMax API and service](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [text, csv]

**Output Format:** [A UTF-8 CSV brief with a conversational summary of key findings.]

**Output Parameters:** [Competitor names, date range, patent jurisdiction, optional technical keywords, and search limits.]

**Other Properties Related to Output:** [Highlights selected patents and technical directions; findings depend on database coverage and should not be treated as an infringement opinion or continuous monitoring.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
