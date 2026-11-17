## Description:

Provides structured information from Anjuke public pages, including property listings, agent rules, services, and help documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to organize public Anjuke real-estate pages, listing services, broker rules, consultation flows, city entries, and help information while preserving source context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public real-estate listing details can vary by city, time, and property, leading to stale or misleading summaries.

Mitigation: Preserve the source page, city, time, property, and listing context, and verify current public Anjuke pages before acting on the summary.

Risk: Requests may seek account-only data, private records, unpublished listings, false-listing packaging, or platform-rule evasion.

Mitigation: Limit use to public pages and refuse private records, backend data, false-listing packaging, account actions, or audit-bypass guidance.

## Reference(s):

- [Anjuke homepage](https://www.anjuke.com/)
- [ClawHub skill page](https://clawhub.ai/mikeclaw007/skills/anjuke)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries and structured lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserve source city, time, property, and page context for real-estate information.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
