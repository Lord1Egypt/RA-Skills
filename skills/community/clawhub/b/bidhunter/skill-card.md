## Description:

Monitors Chinese public and state-owned-enterprise tenders, checks bidder eligibility and bid documents, and prepares procurement reports and alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[419597334-sudo](https://clawhub.ai/user/419597334-sudo)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and bid teams use this skill to monitor Chinese tender notices, compare requirements with their qualifications, track document coverage and scoring, and prepare bid-readiness reports.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Untrusted tender-feed content can enter generated HTML reports.

Mitigation: Avoid opening HTML reports from untrusted or custom feeds until HTML escaping is fixed.

Risk: Unrelated websites can send requests that change the local rule editor.

Mitigation: Run the rule editor only when needed and close it before browsing unrelated sites.

Risk: Optional AI processing may send tender documents to the configured model provider.

Mitigation: Use local-only, non-AI modes unless sharing tender data with that provider is acceptable.

## Reference(s):

- [BidHunter ClawHub release](https://clawhub.ai/419597334-sudo/skills/bidhunter)
- [BidHunter publisher](https://clawhub.ai/user/419597334-sudo)
- [Supported platforms and data sources](artifact/references/platforms.md)
- [Setup guide](artifact/references/setup-guide.md)
- [Qualification and filtering rules](artifact/references/filter_rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, CSV, JSON, Guidance]

**Output Format:** [Text and Markdown reports; optional HTML, CSV, JSON, and XLSX files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes eligibility assessments, scoring and coverage tables, missing-material checklists, compliance warnings, and optional alerts.]

## Skill Version(s):

2.9.1 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
