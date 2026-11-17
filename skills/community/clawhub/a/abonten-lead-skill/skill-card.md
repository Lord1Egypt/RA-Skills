## Description:

Turn photos of offline posters, signboards, flyers, and billboards into a traceable business-lead pipeline: extract visible details, research public business contacts and decision-makers with a bounded TreeBased search, and prepare a Notion dashboard and outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiwithenoch](https://clawhub.ai/user/aiwithenoch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business-development teams use this skill to convert physical advertising images into traceable business leads, public-contact research, Notion-ready records, and reviewed outreach drafts. It is intended for public business information, not private-person discovery or unsolicited outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The lead-research workflow could be misused to research private people or enrich contacts from inappropriate sources.

Mitigation: Use only public business information and public professional contact paths; avoid people-finder sites, leaked datasets, private accounts, personal home addresses, and guessed email patterns.

Risk: Creating or updating a Notion dashboard can modify external records.

Mitigation: Require a clear destination, preview creates and updates, upsert by stable identity keys where possible, and preserve existing manual notes.

Risk: Outbound messages could become unapproved or unsolicited outreach.

Mitigation: Draft by default, show exact recipients and message previews, send only after explicit approval, include opt-out language, and skip Do not contact leads.

## Reference(s):

- [TreeBased Search](references/treebased-search.md)
- [Notion Dashboard](references/notion-dashboard.md)
- [Outreach](references/outreach.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries, lead tables, CSV/JSON fallbacks, Notion-ready records, and outreach drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs preserve source images, raw captures, evidence links, confidence labels, and approval status where applicable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
