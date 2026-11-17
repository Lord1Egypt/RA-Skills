## Description:

Collect public TikTok videos, profiles, comments, sounds, and follower data through the Apify TikTok Scraper, with optional downloads, transcripts, and AI labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshmaur](https://clawhub.ai/user/harshmaur)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social-media researchers use this skill to collect public TikTok content and account data for trend, influencer, campaign, transcript, and brand-safety analysis. Optional features can download media or request AI labels and transcripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scrapes can incur Apify charges, and requested targets and collected data are stored in Apify cloud storage.

Mitigation: Check current pricing, set result and spending caps, and protect the Apify token; account for cloud storage when choosing targets and data.

Risk: Recurring tracking or app delivery may continue spending or expose results to unintended readers.

Mitigation: Require explicit approval of frequency, duration, budget, and the exact delivery destination before enabling recurring runs or app delivery.

## Reference(s):

- [Apify TikTok Scraper MCP server](https://mcp.apify.com/?tools=harshmaur/tiktok-scraper)
- [Apify MCP integration documentation](https://docs.apify.com/platform/integrations/mcp)
- [Usage notes and limitations](references/gotchas.md)

## Skill Output:

**Output Type(s):** [JSON, CSV, Text, MP4 files]

**Output Format:** [JSON or CSV records with concise Markdown summaries; optional MP4 downloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on requested targets, filters, result caps, and enabled transcript or AI options.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
