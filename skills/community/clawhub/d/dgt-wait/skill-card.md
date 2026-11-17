## Description:

Dgt Wait helps users check and report waiting times for practical driving exams across Spanish provinces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jfcanadell](https://clawhub.ai/user/jfcanadell)

### License/Terms of Use:

MIT-0

## Use Case:

External users in Spain use this skill to query community-reported practical driving exam wait times by province and submit their own anonymous wait-time reports.

### Deployment Geography for Use:

Spain

## Known Risks and Mitigations:

Risk: Installation would expose and use a live Supabase database access path and public anonymous key.

Mitigation: Install only after the publisher confirms strict Supabase row-level security, intended public read and insert limits, and no anonymous update or delete access.

Risk: Privacy and persistence disclosures for stored reports and IP-derived limits are incomplete.

Mitigation: Require clear privacy terms, server-side validation, rate limiting, and documented handling of report data and any IP-derived counters before deployment.

## Reference(s):

- [Dgt Wait ClawHub listing](https://clawhub.ai/jfcanadell/skills/dgt-wait)
- [Publisher profile: jfcanadell](https://clawhub.ai/user/jfcanadell)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style conversational responses with wait-time summaries, report confirmations, limit notices, and trust messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include province-specific aggregate statistics, top driving schools by reported wait time, and remaining free-query counts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
