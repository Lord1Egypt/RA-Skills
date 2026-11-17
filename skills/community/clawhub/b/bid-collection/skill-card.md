## Description:

Bid Collection monitors public tender and procurement sources and helps agents identify, rank, and report high-value bid opportunities by business fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptocxf](https://clawhub.ai/user/cryptocxf)

### License/Terms of Use:

MIT-0

## Use Case:

Business development, sales operations, and procurement intelligence teams use this skill to scan public tender sources, monitor selected channels, and generate prioritized lead reports for follow-up.

### Deployment Geography for Use:

Global; source coverage is focused on China public procurement and state-owned enterprise platforms.

## Known Risks and Mitigations:

Risk: Scanning and monitoring send outbound requests to public procurement websites.

Mitigation: Review the target domain list before execution and use only public sources that comply with site terms and access limits.

Risk: Scheduled monitoring can continue making requests and sending notifications after it starts.

Mitigation: Start monitoring only after explicit confirmation, keep the default run limits unless persistence is needed, and stop the monitor when it is no longer required.

Risk: Adding a custom source can direct requests to an untrusted or inappropriate URL.

Mitigation: Add only trusted public procurement platforms and avoid internal, local, metadata, or otherwise sensitive addresses.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/cryptocxf/skills/bid-collection)
- [README](README.md)
- [Quick Start Guide](references/quick-start.md)
- [Tender Lead Matching Rules & Priority Scoring](references/bid-matching-rules.md)
- [Tender & Procurement Monitoring Source List](references/monitoring-sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, configuration, guidance]

**Output Format:** [Markdown reports and structured lead summaries, with optional JSON/HTML files written to the configured local output directory.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scan and monitor outputs are scoped to public procurement information and default to leads-output/bid/.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
