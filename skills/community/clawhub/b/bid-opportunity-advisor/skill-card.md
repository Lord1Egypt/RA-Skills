## Description:

Bid Opportunity Advisor helps procurement teams compare public bid notices with a company profile and produce go/no-go recommendations, fit scores, pricing windows, competitor context, and next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

External procurement, sales, and bid teams use this skill to evaluate whether a specific public tender or category of tenders is worth pursuing. It aligns bid requirements with the user's company profile, explains confidence and data boundaries, and can prepare an action-oriented shortlist or optional HTML report.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill may read or create a local company profile containing business facts.

Mitigation: Keep the profile limited to necessary non-confidential facts and require explicit confirmation before creating or updating ~/.bidprofile.json.

Risk: Procurement searches, direct keyword fetches, or credential-backed sources may send query terms or business intent to external sites.

Mitigation: Require explicit user confirmation before WebSearch, WebFetch, direct --kw fetches, credential use, or API-key-backed retrieval, and avoid confidential strategy in search keywords.

Risk: The skill can save procurement HTML, JSON records, and HTML reports to local files.

Mitigation: Confirm report, profile, and data-file writes before execution and keep generated files in user-approved locations.

Risk: Incomplete public data, login walls, scraping failures, or small sample sizes can make bid recommendations overconfident.

Mitigation: State data boundaries, avoid fabricated fields or confidence scores, and mark recommendations as low confidence when samples are insufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-opportunity-advisor)
- [Data sources and collection strategy](artifact/references/data_sources.md)
- [Decision framework](artifact/references/decision_framework.md)
- [China Government Procurement search](https://search.ccgp.gov.cn/bxsearch)
- [China Tendering and Bidding Public Service bulletin portal](https://bulletin.cebpubservice.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON records, HTML reports, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read or create a local company profile only with user consent, and may save procurement HTML, JSON, and report files during analysis.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
